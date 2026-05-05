from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import base64, hashlib, json, math, os, shutil, socket, struct, subprocess, time, urllib.request

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "app/videos/20260505_guide_scroll"
FRAMES = OUT / "frames_cdp"
QA = OUT / "qa"
OUT.mkdir(parents=True, exist_ok=True)
QA.mkdir(parents=True, exist_ok=True)

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FPS_CAPTURE = 12
FPS_OUT = 30
FONT_DIR = Path.home() / "Library/Fonts"
FONT_SEMI = str(FONT_DIR / "SUIT-SemiBold.otf")


def free_port():
    s=socket.socket(); s.bind(("127.0.0.1",0)); p=s.getsockname()[1]; s.close(); return p


def wait_url(url, timeout=8):
    t=time.time()
    while time.time()-t<timeout:
        try:
            with urllib.request.urlopen(url, timeout=1) as r:
                return r.read().decode()
        except Exception:
            time.sleep(.1)
    raise RuntimeError(f"timeout waiting {url}")


def start_http():
    p=free_port()
    proc=subprocess.Popen(["python3","-m","http.server",str(p),"--bind","127.0.0.1"], cwd=str(ROOT), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    wait_url(f"http://127.0.0.1:{p}/guides/index.html")
    return proc,p


def start_chrome():
    port=free_port()
    user_dir=OUT/"chrome-cdp-profile"
    if user_dir.exists(): shutil.rmtree(user_dir)
    cmd=[CHROME,"--headless=new",f"--remote-debugging-port={port}",f"--user-data-dir={user_dir}","--no-first-run","--disable-extensions","--disable-gpu","--hide-scrollbars","about:blank"]
    proc=subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    wait_url(f"http://127.0.0.1:{port}/json/version")
    return proc,port


class WS:
    def __init__(self, url):
        assert url.startswith('ws://')
        hostport_path=url[5:]
        hostport,path=hostport_path.split('/',1)
        if ':' in hostport:
            host,port=hostport.split(':',1); port=int(port)
        else:
            host,port=hostport,80
        self.sock=socket.create_connection((host,port), timeout=5)
        key=base64.b64encode(os.urandom(16)).decode()
        req=(f"GET /{path} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n")
        self.sock.sendall(req.encode())
        resp=b''
        while b'\r\n\r\n' not in resp:
            resp+=self.sock.recv(4096)
        if b' 101 ' not in resp.split(b'\r\n',1)[0]:
            raise RuntimeError(resp[:200])
        self.next_id=1
        self.pending={}
    def send_json(self,obj):
        data=json.dumps(obj,separators=(',',':')).encode()
        header=bytearray([0x81])
        ln=len(data)
        if ln<126: header.append(0x80|ln)
        elif ln<65536: header += bytes([0x80|126]) + struct.pack('!H',ln)
        else: header += bytes([0x80|127]) + struct.pack('!Q',ln)
        mask=os.urandom(4); header+=mask
        masked=bytes(b ^ mask[i%4] for i,b in enumerate(data))
        self.sock.sendall(header+masked)
    def recv_json(self):
        def recvn(n):
            b=b''
            while len(b)<n:
                chunk=self.sock.recv(n-len(b))
                if not chunk: raise EOFError
                b+=chunk
            return b
        h=recvn(2); b1,b2=h[0],h[1]
        ln=b2&0x7f
        if ln==126: ln=struct.unpack('!H',recvn(2))[0]
        elif ln==127: ln=struct.unpack('!Q',recvn(8))[0]
        masked=b2&0x80
        mask=recvn(4) if masked else b''
        payload=recvn(ln)
        if masked: payload=bytes(c ^ mask[i%4] for i,c in enumerate(payload))
        if b1&0x0f==8: raise EOFError
        if b1&0x0f not in (1,2): return self.recv_json()
        return json.loads(payload.decode())
    def call(self, method, params=None, timeout=8):
        i=self.next_id; self.next_id+=1
        self.send_json({"id":i,"method":method,"params":params or {}})
        t=time.time()
        while time.time()-t<timeout:
            msg=self.recv_json()
            if msg.get('id')==i:
                if 'error' in msg: raise RuntimeError(msg['error'])
                return msg.get('result',{})
        raise TimeoutError(method)
    def close(self):
        try: self.sock.close()
        except Exception: pass


def new_page(chrome_port):
    # Chrome 147 expects PUT for /json/new
    req=urllib.request.Request(f"http://127.0.0.1:{chrome_port}/json/new", method='PUT')
    with urllib.request.urlopen(req) as r:
        info=json.loads(r.read().decode())
    ws=WS(info['webSocketDebuggerUrl'])
    ws.call('Page.enable')
    ws.call('Runtime.enable')
    return ws


def navigate(ws, url):
    ws.call('Page.navigate', {'url': url})
    time.sleep(1.0)


def set_view(ws, width, height, scale=1, mobile=False):
    ws.call('Emulation.setDeviceMetricsOverride', {'width':width,'height':height,'deviceScaleFactor':scale,'mobile':mobile})
    ws.call('Emulation.setVisibleSize', {'width':width,'height':height})


def eval_js(ws, expr):
    return ws.call('Runtime.evaluate', {'expression': expr, 'returnByValue': True}).get('result',{}).get('value')


def capture(ws, out_path):
    res=ws.call('Page.captureScreenshot', {'format':'png','fromSurface':True,'captureBeyondViewport':False}, timeout=12)
    out_path.write_bytes(base64.b64decode(res['data']))


def path_values(max_y, seconds, fps):
    n=int(seconds*fps)
    vals=[]
    for i in range(n):
        t=i/max(1,n-1)
        # 인간처럼: 아래로 훑고, 살짝 올려 확인하고, 다시 내려감
        if t<0.62:
            u=t/0.62; y=max_y*0.68*(0.5-0.5*math.cos(math.pi*u))
        elif t<0.78:
            u=(t-0.62)/0.16; y=max_y*(0.68-0.16*(0.5-0.5*math.cos(math.pi*u)))
        else:
            u=(t-0.78)/0.22; y=max_y*(0.52+0.34*(0.5-0.5*math.cos(math.pi*u)))
        vals.append(int(y))
    return vals


def font(size):
    return ImageFont.truetype(FONT_SEMI, size)


def caption(im, text, vertical):
    if not text: return im
    W,H=im.size
    layer=Image.new('RGBA', im.size, (0,0,0,0)); d=ImageDraw.Draw(layer)
    f=font(34 if vertical else 25)
    bbox=d.textbbox((0,0), text, font=f); tw,th=bbox[2]-bbox[0],bbox[3]-bbox[1]
    x=(W-tw)//2; y=H-th-(96 if vertical else 42)
    px,py=(30,16) if vertical else (22,12)
    d.rounded_rectangle((x-px,y-py,x+tw+px,y+th+py), radius=28, fill=(18,20,30,135))
    d.text((x,y), text, font=f, fill=(255,255,255,245))
    out=im.convert('RGBA'); out.alpha_composite(layer); return out.convert('RGB')


def make_video(chrome_port, http_port, name, page, metrics, final_size, seconds, max_scroll_ratio, cap_text, vertical):
    frame_dir=FRAMES/name
    if frame_dir.exists(): shutil.rmtree(frame_dir)
    frame_dir.mkdir(parents=True)
    ws=new_page(chrome_port)
    try:
        set_view(ws, *metrics)
        url=f"http://127.0.0.1:{http_port}{page}"
        navigate(ws, url)
        # 강제로 라이트 모드 + 자동 스크롤 제거
        eval_js(ws, "document.documentElement.setAttribute('data-theme','light'); document.documentElement.style.scrollBehavior='auto'; document.body.style.scrollBehavior='auto';")
        time.sleep(.4)
        max_y=eval_js(ws, "Math.max(0, document.documentElement.scrollHeight - window.innerHeight)") or 0
        max_y=int(max_y*max_scroll_ratio)
        ys=path_values(max_y, seconds, FPS_CAPTURE)
        for i,y in enumerate(ys):
            eval_js(ws, f"window.scrollTo(0,{y});")
            time.sleep(0.025)
            png=frame_dir/f"shot_{i:04d}.png"
            capture(ws, png)
            im=Image.open(png).convert('RGB')
            if im.size != final_size:
                im=im.resize(final_size, Image.Resampling.LANCZOS)
            im=caption(im, cap_text, vertical)
            im.save(frame_dir/f"frame_{i:04d}.jpg", quality=94, optimize=True)
            png.unlink(missing_ok=True)
    finally:
        ws.close()
    out=OUT/f"{name}.mp4"
    subprocess.run([
        'ffmpeg','-y','-framerate',str(FPS_CAPTURE),'-i',str(frame_dir/'frame_%04d.jpg'),
        '-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=44100','-shortest',
        '-vf',f'fps={FPS_OUT},scale=in_range=pc:out_range=tv,format=yuv420p',
        '-c:v','libx264','-crf','20','-profile:v','high','-movflags','+faststart','-c:a','aac','-b:a','96k',str(out)
    ], check=True)
    return out


def qa(video, out_img, times, thumb_w):
    imgs=[]
    for idx,t in enumerate(times):
        p=QA/f"tmp_{out_img.stem}_{idx}.jpg"
        subprocess.run(['ffmpeg','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(p)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        im=Image.open(p).convert('RGB'); r=thumb_w/im.width; im=im.resize((thumb_w,int(im.height*r)), Image.Resampling.LANCZOS); imgs.append(im); p.unlink()
    sheet=Image.new('RGB',(sum(i.width for i in imgs),max(i.height for i in imgs)),(245,245,250))
    x=0
    for im in imgs: sheet.paste(im,(x,0)); x+=im.width
    sheet.save(out_img, quality=92)


def main():
    http_proc=http_port=chrome_proc=chrome_port=None
    http_proc,http_port=start_http()
    chrome_proc,chrome_port=start_chrome()
    try:
        # 모바일 CSS viewport 430x764를 DPR로 1080x1920에 가깝게 캡처
        vertical=make_video(
            chrome_port,http_port,
            'nodev-guide-real-scroll-instagram-9x16-no-caption',
            '/guides/guide-02-claude-code-install.html',
            (430,764,1080/430,True),
            (1080,1920),
            11.5,0.55,
            '',True)
        horizontal=make_video(
            chrome_port,http_port,
            'nodev-guide-real-scroll-threads-16x9',
            '/guides/index.html',
            (1280,720,1,False),
            (1280,720),
            11.5,0.85,
            '가이드 페이지를 먼저 훑어보세요',False)
        qa(vertical, QA/'instagram-real-scroll-midpoints.jpg', [0.8,2.8,5.2,7.8,10.3], 240)
        qa(horizontal, QA/'threads-real-scroll-midpoints.jpg', [0.8,2.8,5.2,7.8,10.3], 300)
        for f in [vertical,horizontal,QA/'instagram-real-scroll-midpoints.jpg',QA/'threads-real-scroll-midpoints.jpg']:
            print(f, f.stat().st_size)
    finally:
        for p in [chrome_proc,http_proc]:
            if p:
                p.terminate()
                try: p.wait(timeout=2)
                except subprocess.TimeoutExpired: p.kill()

if __name__=='__main__': main()
