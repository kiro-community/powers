# AgentCore Browser Usage Examples

Real-world examples of using AgentCore Browser for various automation tasks.

## Example 1: Simple Web Scraping

Extract product information from an e-commerce site:

```python
# Create session
await create_browser_session(
    session_id="product-scraper",
    description="Scraping product data"
)

# Navigate to product page
await navigate(
    session_id="product-scraper",
    url="https://example-shop.com/products/laptop"
)

# Extract product name
product_name = await extract_content(
    session_id="product-scraper",
    content_type="text",
    selector="h1.product-title"
)

# Extract price
price = await extract_content(
    session_id="product-scraper",
    content_type="text",
    selector="span.price"
)

# Extract description
description = await extract_content(
    session_id="product-scraper",
    content_type="text",
    selector="div.product-description"
)

# Take screenshot for verification
await screenshot(
    session_id="product-scraper",
    path="product-page.png"
)

# Close session
await close_session(session_id="product-scraper")

print(f"Product: {product_name}")
print(f"Price: {price}")
print(f"Description: {description}")
```

## Example 2: Form Submission with Validation

Submit a contact form and verify success:

```python
# Create session
await create_browser_session(
    session_id="contact-form",
    description="Contact form submission"
)

# Navigate to contact page
await navigate(
    session_id="contact-form",
    url="https://example.com/contact"
)

# Fill form fields
await interact(
    session_id="contact-form",
    action="type",
    selector="input[name='name']",
    text="John Doe"
)

await interact(
    session_id="contact-form",
    action="type",
    selector="input[name='email']",
    text="john.doe@example.com"
)

await interact(
    session_id="contact-form",
    action="type",
    selector="input[name='phone']",
    text="+1-555-0123"
)

await interact(
    session_id="contact-form",
    action="type",
    selector="textarea[name='message']",
    text="I would like to inquire about your services."
)

# Take screenshot before submission
await screenshot(
    session_id="contact-form",
    path="form-filled.png"
)

# Submit form
await interact(
    session_id="contact-form",
    action="click",
    selector="button[type='submit']"
)

# Wait for submission to complete
await execute_script(
    session_id="contact-form",
    script="await new Promise(r => setTimeout(r, 2000))"
)

# Verify success message
success_message = await extract_content(
    session_id="contact-form",
    content_type="text",
    selector="div.success-message"
)

# Take screenshot of result
await screenshot(
    session_id="contact-form",
    path="form-submitted.png"
)

# Close session
await close_session(session_id="contact-form")

print(f"Submission result: {success_message}")
```

## Example 3: Login and Navigate Protected Pages

Authenticate and access protected content:

```python
# Create session
await create_browser_session(
    session_id="authenticated-session",
    description="Login and access protected pages",
    session_timeout=7200  # 2 hours for extended session
)

# Navigate to login page
await navigate(
    session_id="authenticated-session",
    url="https://example.com/login"
)

# Enter credentials
await interact(
    session_id="authenticated-session",
    action="type",
    selector="input[name='username']",
    text="user@example.com"
)

await interact(
    session_id="authenticated-session",
    action="type",
    selector="input[name='password']",
    text="secure-password"
)

# Click login button
await interact(
    session_id="authenticated-session",
    action="click",
    selector="button[type='submit']"
)

# Wait for redirect
await execute_script(
    session_id="authenticated-session",
    script="await new Promise(r => setTimeout(r, 2000))"
)

# Now authenticated - navigate to dashboard
await navigate(
    session_id="authenticated-session",
    url="https://example.com/dashboard"
)

# Extract user info
user_name = await extract_content(
    session_id="authenticated-session",
    content_type="text",
    selector="span.user-name"
)

# Navigate to profile (still authenticated)
await navigate(
    session_id="authenticated-session",
    url="https://example.com/profile"
)

# Extract profile data
profile_data = await execute_script(
    session_id="authenticated-session",
    script="""
    return {
        name: document.querySelector('.profile-name').textContent,
        email: document.querySelector('.profile-email').textContent,
        memberSince: document.querySelector('.member-since').textContent
    };
    """
)

# Close session
await close_session(session_id="authenticated-session")

print(f"Logged in as: {user_name}")
print(f"Profile: {profile_data}")
```

## Example 4: Multi-Tab Price Comparison

Compare prices across multiple websites:

```python
# Create session
await create_browser_session(
    session_id="price-comparison",
    description="Comparing prices across sites"
)

# Site 1 (main tab)
await navigate(
    session_id="price-comparison",
    url="https://site1.com/product/laptop-xyz"
)

price1 = await extract_content(
    session_id="price-comparison",
    content_type="text",
    selector="span.price"
)

# Site 2 (new tab)
await manage_tabs(
    session_id="price-comparison",
    action="new_tab",
    tab_id="site2"
)

await navigate(
    session_id="price-comparison",
    url="https://site2.com/products/laptop-xyz"
)

price2 = await extract_content(
    session_id="price-comparison",
    content_type="text",
    selector="div.product-price"
)

# Site 3 (new tab)
await manage_tabs(
    session_id="price-comparison",
    action="new_tab",
    tab_id="site3"
)

await navigate(
    session_id="price-comparison",
    url="https://site3.com/item/laptop-xyz"
)

price3 = await extract_content(
    session_id="price-comparison",
    content_type="text",
    selector="span.current-price"
)

# Compare prices
prices = {
    "Site 1": price1,
    "Site 2": price2,
    "Site 3": price3
}

# Close session
await close_session(session_id="price-comparison")

print("Price Comparison:")
for site, price in prices.items():
    print(f"{site}: {price}")
```

## Example 5: Automated Testing

Test a web application's functionality:

```python
# Create session with recording for test evidence
await create_browser_session(
    session_id="qa-test-login",
    description="QA test: Login functionality",
    enable_recording=True
)

# Test Case 1: Valid Login
await navigate(
    session_id="qa-test-login",
    url="https://app.example.com/login"
)

await interact(
    session_id="qa-test-login",
    action="type",
    selector="input#email",
    text="test@example.com"
)

await interact(
    session_id="qa-test-login",
    action="type",
    selector="input#password",
    text="ValidPassword123"
)

await screenshot(
    session_id="qa-test-login",
    path="test-login-filled.png"
)

await interact(
    session_id="qa-test-login",
    action="click",
    selector="button#login-btn"
)

# Verify successful login
await execute_script(
    session_id="qa-test-login",
    script="await new Promise(r => setTimeout(r, 2000))"
)

current_url = await execute_script(
    session_id="qa-test-login",
    script="return window.location.href"
)

assert "/dashboard" in current_url, "Login failed - not redirected to dashboard"

await screenshot(
    session_id="qa-test-login",
    path="test-login-success.png"
)

# Test Case 2: Logout
await interact(
    session_id="qa-test-login",
    action="click",
    selector="button#logout-btn"
)

await execute_script(
    session_id="qa-test-login",
    script="await new Promise(r => setTimeout(r, 1000))"
)

current_url = await execute_script(
    session_id="qa-test-login",
    script="return window.location.href"
)

assert "/login" in current_url, "Logout failed - not redirected to login"

await screenshot(
    session_id="qa-test-login",
    path="test-logout-success.png"
)

# Close session (recording saved to S3)
await close_session(session_id="qa-test-login")

print("✅ All tests passed!")
```

## Example 6: Data Collection with Pagination

Scrape data across multiple pages:

```python
# Create session
await create_browser_session(
    session_id="paginated-scraper",
    description="Scraping paginated data",
    session_timeout=7200  # 2 hours for large dataset
)

all_products = []
page = 1
max_pages = 10

while page <= max_pages:
    # Navigate to page
    await navigate(
        session_id="paginated-scraper",
        url=f"https://example.com/products?page={page}"
    )
    
    # Extract products from current page
    products = await execute_script(
        session_id="paginated-scraper",
        script="""
        return Array.from(document.querySelectorAll('.product')).map(p => ({
            name: p.querySelector('.name').textContent,
            price: p.querySelector('.price').textContent,
            rating: p.querySelector('.rating').textContent
        }));
        """
    )
    
    all_products.extend(products)
    
    # Check if next page exists
    has_next = await execute_script(
        session_id="paginated-scraper",
        script="return document.querySelector('.next-page') !== null"
    )
    
    if not has_next:
        break
    
    page += 1
    
    # Be polite - wait between requests
    await execute_script(
        session_id="paginated-scraper",
        script="await new Promise(r => setTimeout(r, 1000))"
    )

# Close session
await close_session(session_id="paginated-scraper")

print(f"Collected {len(all_products)} products from {page} pages")
```

## Example 7: Monitoring Website Changes

Check if website content has changed:

```python
# Create session
await create_browser_session(
    session_id="change-monitor",
    description="Monitoring website for changes"
)

# Navigate to page
await navigate(
    session_id="change-monitor",
    url="https://example.com/status"
)

# Extract current content
current_content = await extract_content(
    session_id="change-monitor",
    content_type="text",
    selector="div.status-message"
)

# Take screenshot
await screenshot(
    session_id="change-monitor",
    path="status-current.png"
)

# Compare with previous content (loaded from file/database)
previous_content = load_previous_content()  # Your function

if current_content != previous_content:
    print("⚠️ Content has changed!")
    print(f"Previous: {previous_content}")
    print(f"Current: {current_content}")
    
    # Send alert (your notification logic)
    send_alert(f"Website changed: {current_content}")
else:
    print("✅ No changes detected")

# Save current content for next check
save_content(current_content)  # Your function

# Close session
await close_session(session_id="change-monitor")
```

## Example 8: Handling Dynamic Content

Work with JavaScript-heavy single-page applications:

```python
# Create session
await create_browser_session(
    session_id="spa-interaction",
    description="Interacting with SPA"
)

# Navigate to SPA
await navigate(
    session_id="spa-interaction",
    url="https://example.com/app"
)

# Wait for React/Vue/Angular to load
await execute_script(
    session_id="spa-interaction",
    script="await new Promise(r => setTimeout(r, 3000))"
)

# Click button that triggers AJAX request
await interact(
    session_id="spa-interaction",
    action="click",
    selector="button.load-data"
)

# Wait for AJAX to complete
await execute_script(
    session_id="spa-interaction",
    script="""
    await new Promise(resolve => {
        const checkData = () => {
            if (document.querySelector('.data-loaded')) {
                resolve();
            } else {
                setTimeout(checkData, 100);
            }
        };
        checkData();
    });
    """
)

# Extract dynamically loaded data
data = await extract_content(
    session_id="spa-interaction",
    content_type="text",
    selector="div.dynamic-content"
)

# Close session
await close_session(session_id="spa-interaction")

print(f"Dynamic data: {data}")
```

## Tips for Real-World Usage

### 1. Error Handling

Always wrap automation in try-except:

```python
try:
    await create_browser_session(...)
    await navigate(...)
    await interact(...)
except Exception as e:
    print(f"Error: {e}")
    await screenshot(session_id="session", path="error.png")
finally:
    await close_session(session_id="session")
```

### 2. Retries

Implement retry logic for flaky operations:

```python
max_retries = 3
for attempt in range(max_retries):
    try:
        await interact(session_id="session", action="click", selector="button")
        break
    except Exception as e:
        if attempt == max_retries - 1:
            raise
        await execute_script(
            session_id="session",
            script="await new Promise(r => setTimeout(r, 1000))"
        )
```

### 3. Logging

Log important steps:

```python
print(f"[{datetime.now()}] Creating session...")
await create_browser_session(...)

print(f"[{datetime.now()}] Navigating to {url}...")
await navigate(...)

print(f"[{datetime.now()}] Extracting data...")
data = await extract_content(...)
```

### 4. Rate Limiting

Be respectful to websites:

```python
for url in urls:
    await navigate(session_id="session", url=url)
    # Extract data...
    
    # Wait between requests
    await execute_script(
        session_id="session",
        script="await new Promise(r => setTimeout(r, 2000))"
    )
```

## Next Steps

- Read `session-management.md` for advanced session techniques
- Check `troubleshooting.md` for common issues
- Review `web-automation-patterns.md` for more patterns
