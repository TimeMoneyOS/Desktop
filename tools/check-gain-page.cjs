const {chromium}=require(process.env.PLAYWRIGHT_MODULE);
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 for(const width of [1440,390]){
  const page=await browser.newPage({viewport:{width,height:900}});
  await page.goto('http://127.0.0.1:8008/gain-link/');
  await page.locator('article img').first().waitFor();
  const result=await page.evaluate(()=>({title:document.querySelector('h1').textContent,images:[...document.querySelectorAll('article img')].map(i=>i.complete&&i.naturalWidth>0),overflow:document.documentElement.scrollWidth>innerWidth}));
  if(result.overflow||result.images.some(v=>!v)||result.images.length!==6)throw Error(JSON.stringify(result));
  await page.screenshot({path:`gain-page-${width}.png`,fullPage:false});
  console.log(width,result);await page.close();
 }
 await browser.close();
})();
