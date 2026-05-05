const { chromium } = require('playwright');
const path = require('path');
(async()=>{
  const root='/Users/jinsik/Desktop/Workspace/01_project_threads/app/cards/layout-templates/20260501_mobileeditingclub_reference';
  const browser=await chromium.launch({headless:true});
  const page=await browser.newPage({viewport:{width:2160,height:7200},deviceScaleFactor:1});
  await page.goto('file://'+path.join(root,'layout-template-board.html'));
  await page.screenshot({path:path.join(root,'layout-template-board.png'),fullPage:true});
  await browser.close();
})();
