import asyncio
from playwright.async_api import async_playwright

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # Set a standard viewport for the dashboard screenshot
        await page.set_viewport_size({"width": 1600, "height": 1000})
        
        await page.goto("http://localhost:8502")
        print("Waiting for dashboard to load...")
        # Wait for Streamlit to finish rendering the initial app
        await page.wait_for_timeout(7000)
        
        # Take the dashboard screenshot
        await page.screenshot(path="images/dashboard_sample.png")
        print("Captured dashboard_sample.png")
        
        try:
            print("Clicking the Run Compliance Simulation button...")
            await page.click("button:has-text('Run Compliance Simulation')", timeout=5000)
            
            # Wait for the spinner to disappear and the heatmap/results to render
            print("Waiting for simulation results...")
            await page.wait_for_timeout(10000)
            
            # Scroll the heatmap into view using partial text matching
            await page.locator('h3:has-text("Water Quality Heatmap")').scroll_into_view_if_needed()
            await page.wait_for_timeout(1000)
            
            # Take the output screenshot (not full page)
            await page.screenshot(path="images/output_sample.png")
            print("Captured output_sample.png")
        except Exception as e:
            print(f"Error while running simulation or capturing output: {e}")
        
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture())
