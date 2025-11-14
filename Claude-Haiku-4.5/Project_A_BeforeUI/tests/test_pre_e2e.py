"""E2E tests for Project A (Before) - UI interaction and visual validation."""

import json
import asyncio
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import subprocess
import sys

try:
    from playwright.async_api import async_playwright, expect
except ImportError:
    print("Playwright not installed. Install with: pip install playwright")
    sys.exit(1)

# Configuration
BASE_URL = "http://localhost:3000"
SCREENSHOT_DIR = Path(__file__).parent.parent / "screenshots"
LOGS_DIR = Path(__file__).parent.parent / "logs"
RESULTS_DIR = Path(__file__).parent.parent / "results"

# Create directories if they don't exist
SCREENSHOT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# Load test data
TEST_DATA_PATH = Path(__file__).parent.parent.parent / "test_data.json"
with open(TEST_DATA_PATH, encoding='utf-8') as f:
    TEST_DATA = json.load(f)

class E2ETestRunner:
    """Run E2E tests with Playwright."""
    
    def __init__(self):
        self.results = []
        self.logs = []
        self.start_time = time.time()
    
    async def run_tests(self):
        """Run all E2E tests."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            
            # Set viewport
            await page.set_viewport_size({"width": 1280, "height": 800})
            
            try:
                # Test 1: Normal UI state
                await self.test_normal_ui_state(page)
                
                # Test 2: Dense layout with long text
                await self.test_dense_layout(page)
                
                # Test 3: Interaction - add task
                await self.test_add_task(page)
                
                # Test 4: Interaction - delete task
                await self.test_delete_task(page)
                
                # Test 5: Hover feedback
                await self.test_hover_feedback(page)
                
                # Test 6: Checkbox interaction
                await self.test_checkbox_interaction(page)
                
                # Test 7: Responsive layout
                await self.test_responsive_layout(page)
                
            finally:
                await browser.close()
        
        # Save results
        self.save_results()
    
    async def test_normal_ui_state(self, page):
        """Test normal UI state and initial rendering."""
        test_id = "test_normal_ui_state"
        self.log(f"Starting: {test_id}")
        
        try:
            await page.goto(BASE_URL, wait_until="networkidle")
            
            # Take screenshot
            screenshot_path = SCREENSHOT_DIR / f"screenshot_pre_{test_id}.png"
            await page.screenshot(path=str(screenshot_path))
            self.log(f"  Screenshot: {screenshot_path}")
            
            # Verify DOM structure
            task_items = await page.locator(".task-item").count()
            self.log(f"  Found {task_items} task items")
            
            # Verify input field exists
            input_field = await page.locator("#taskInput").count()
            self.log(f"  Input field exists: {input_field > 0}")
            
            # Verify add button exists
            add_btn = await page.locator("#addBtn").count()
            self.log(f"  Add button exists: {add_btn > 0}")
            
            self.results.append({
                "test_id": test_id,
                "status": "PASSED",
                "task_items": task_items,
                "screenshot": str(screenshot_path),
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            self.log(f"  ERROR: {str(e)}")
            self.results.append({
                "test_id": test_id,
                "status": "FAILED",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
    
    async def test_dense_layout(self, page):
        """Test layout with long text."""
        test_id = "test_dense_layout_long_text"
        self.log(f"Starting: {test_id}")
        
        try:
            await page.goto(BASE_URL)
            
            # Find a task with long text (second task)
            task_title = await page.locator(".task-title").nth(1).text_content()
            self.log(f"  Task text length: {len(task_title)}")
            
            # Take screenshot
            screenshot_path = SCREENSHOT_DIR / f"screenshot_pre_{test_id}.png"
            await page.screenshot(path=str(screenshot_path))
            
            # Check if text wraps properly
            bounding_box = await page.locator(".task-title").nth(1).bounding_box()
            self.log(f"  Task title bounding box: {bounding_box}")
            
            # Verify no horizontal scrollbar
            scroll_width = await page.evaluate("document.documentElement.scrollWidth")
            client_width = await page.evaluate("document.documentElement.clientWidth")
            has_horizontal_scroll = scroll_width > client_width
            
            self.results.append({
                "test_id": test_id,
                "status": "PASSED",
                "has_horizontal_scroll": has_horizontal_scroll,
                "screenshot": str(screenshot_path)
            })
            
        except Exception as e:
            self.log(f"  ERROR: {str(e)}")
            self.results.append({
                "test_id": test_id,
                "status": "FAILED",
                "error": str(e)
            })
    
    async def test_add_task(self, page):
        """Test adding a new task."""
        test_id = "test_add_task"
        self.log(f"Starting: {test_id}")
        
        try:
            await page.goto(BASE_URL)
            
            # Get initial task count
            initial_count = await page.locator(".task-item").count()
            self.log(f"  Initial tasks: {initial_count}")
            
            # Type in input
            await page.fill("#taskInput", "New test task")
            
            # Click add button
            await page.click("#addBtn")
            
            # Wait for new task to appear
            await page.wait_for_selector(".task-item", timeout=2000)
            
            # Get new task count
            await asyncio.sleep(0.5)
            new_count = await page.locator(".task-item").count()
            self.log(f"  Tasks after add: {new_count}")
            
            # Take screenshot
            screenshot_path = SCREENSHOT_DIR / f"screenshot_pre_{test_id}.png"
            await page.screenshot(path=str(screenshot_path))
            
            self.results.append({
                "test_id": test_id,
                "status": "PASSED" if new_count > initial_count else "FAILED",
                "initial_count": initial_count,
                "final_count": new_count,
                "screenshot": str(screenshot_path)
            })
            
        except Exception as e:
            self.log(f"  ERROR: {str(e)}")
            self.results.append({
                "test_id": test_id,
                "status": "FAILED",
                "error": str(e)
            })
    
    async def test_delete_task(self, page):
        """Test deleting a task."""
        test_id = "test_delete_task"
        self.log(f"Starting: {test_id}")
        
        try:
            await page.goto(BASE_URL)
            
            initial_count = await page.locator(".task-item").count()
            self.log(f"  Initial tasks: {initial_count}")
            
            # Click first delete button
            if initial_count > 0:
                await page.click(".delete-btn:first-of-type")
                
                # Wait a bit for deletion
                await asyncio.sleep(0.5)
                
                new_count = await page.locator(".task-item").count()
                self.log(f"  Tasks after delete: {new_count}")
                
                # Take screenshot
                screenshot_path = SCREENSHOT_DIR / f"screenshot_pre_{test_id}.png"
                await page.screenshot(path=str(screenshot_path))
                
                self.results.append({
                    "test_id": test_id,
                    "status": "PASSED" if new_count < initial_count else "FAILED",
                    "initial_count": initial_count,
                    "final_count": new_count,
                    "screenshot": str(screenshot_path)
                })
            else:
                self.results.append({
                    "test_id": test_id,
                    "status": "SKIPPED",
                    "reason": "No tasks to delete"
                })
            
        except Exception as e:
            self.log(f"  ERROR: {str(e)}")
            self.results.append({
                "test_id": test_id,
                "status": "FAILED",
                "error": str(e)
            })
    
    async def test_hover_feedback(self, page):
        """Test hover feedback on interactive elements."""
        test_id = "test_hover_feedback"
        self.log(f"Starting: {test_id}")
        
        try:
            await page.goto(BASE_URL)
            
            # Hover over delete button
            delete_btn = page.locator(".delete-btn").first
            await delete_btn.hover()
            
            # Get computed style
            hover_color = await delete_btn.evaluate(
                "el => window.getComputedStyle(el).backgroundColor"
            )
            self.log(f"  Delete button hover color: {hover_color}")
            
            # Take screenshot
            screenshot_path = SCREENSHOT_DIR / f"screenshot_pre_{test_id}_hover.png"
            await page.screenshot(path=str(screenshot_path))
            
            # Hover over task item
            task_item = page.locator(".task-item").first
            await task_item.hover()
            
            task_hover_bg = await task_item.evaluate(
                "el => window.getComputedStyle(el).backgroundColor"
            )
            self.log(f"  Task item hover background: {task_hover_bg}")
            
            self.results.append({
                "test_id": test_id,
                "status": "PASSED",
                "delete_btn_hover_color": hover_color,
                "task_item_hover_bg": task_hover_bg,
                "screenshot": str(screenshot_path)
            })
            
        except Exception as e:
            self.log(f"  ERROR: {str(e)}")
            self.results.append({
                "test_id": test_id,
                "status": "FAILED",
                "error": str(e)
            })
    
    async def test_checkbox_interaction(self, page):
        """Test checkbox functionality."""
        test_id = "test_checkbox_interaction"
        self.log(f"Starting: {test_id}")
        
        try:
            await page.goto(BASE_URL)
            
            checkbox = page.locator(".task-checkbox").first
            
            # Check initial state
            is_checked_before = await checkbox.is_checked()
            self.log(f"  Checkbox checked before: {is_checked_before}")
            
            # Click checkbox
            await checkbox.click()
            
            # Check state after click
            is_checked_after = await checkbox.is_checked()
            self.log(f"  Checkbox checked after: {is_checked_after}")
            
            # Take screenshot
            screenshot_path = SCREENSHOT_DIR / f"screenshot_pre_{test_id}.png"
            await page.screenshot(path=str(screenshot_path))
            
            self.results.append({
                "test_id": test_id,
                "status": "PASSED",
                "checked_before": is_checked_before,
                "checked_after": is_checked_after,
                "screenshot": str(screenshot_path)
            })
            
        except Exception as e:
            self.log(f"  ERROR: {str(e)}")
            self.results.append({
                "test_id": test_id,
                "status": "FAILED",
                "error": str(e)
            })
    
    async def test_responsive_layout(self, page):
        """Test responsive layout at different viewport sizes."""
        test_id = "test_responsive_layout"
        self.log(f"Starting: {test_id}")
        
        try:
            viewports = [
                {"width": 1280, "height": 800, "name": "desktop"},
                {"width": 768, "height": 1024, "name": "tablet"},
                {"width": 375, "height": 667, "name": "mobile"},
            ]
            
            for vp in viewports:
                await page.set_viewport_size({"width": vp["width"], "height": vp["height"]})
                await page.goto(BASE_URL)
                
                # Take screenshot
                screenshot_path = SCREENSHOT_DIR / f"screenshot_pre_{test_id}_{vp['name']}.png"
                await page.screenshot(path=str(screenshot_path))
                self.log(f"  Screenshot at {vp['name']}: {screenshot_path}")
            
            self.results.append({
                "test_id": test_id,
                "status": "PASSED",
                "viewports_tested": [v["name"] for v in viewports]
            })
            
        except Exception as e:
            self.log(f"  ERROR: {str(e)}")
            self.results.append({
                "test_id": test_id,
                "status": "FAILED",
                "error": str(e)
            })
    
    def log(self, message):
        """Add message to logs."""
        timestamp = datetime.now().isoformat()
        log_line = f"[{timestamp}] {message}"
        self.logs.append(log_line)
        print(log_line)
    
    def save_results(self):
        """Save results to JSON and logs to file."""
        # Save results JSON
        results_file = RESULTS_DIR / "results_pre.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        self.log(f"Results saved to: {results_file}")
        
        # Save logs
        logs_file = LOGS_DIR / "log_pre.txt"
        with open(logs_file, 'w') as f:
            f.write("\n".join(self.logs))
        self.log(f"Logs saved to: {logs_file}")
        
        # Save timing
        elapsed_time = time.time() - self.start_time
        time_file = RESULTS_DIR / "time_pre.txt"
        with open(time_file, 'w') as f:
            f.write(f"Total execution time: {elapsed_time:.2f} seconds\n")
        
        self.log(f"Execution time: {elapsed_time:.2f}s")


async def main():
    """Main entry point."""
    runner = E2ETestRunner()
    await runner.run_tests()


if __name__ == "__main__":
    asyncio.run(main())
