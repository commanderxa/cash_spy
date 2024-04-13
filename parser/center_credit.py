from playwright.sync_api import sync_playwright
import re


def parse_div_text_by_class(url, class_name):
    # Launch the browser
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # Create a new browser context
        context = browser.new_context()
        
        # Open a new page
        page = context.new_page()
        
        # Navigate to the URL
        page.goto(url)
        
        # Wait for the divs with the specified class name to load
        page.wait_for_selector(f'div.{class_name}')
        
        # Get all divs with the specified class name
        divs = page.query_selector_all(f'div.{class_name}')
        
        # Extract text from each div
        div_texts = [div.inner_text() for div in divs]
        
        # Close the browser
        browser.close()
        
        return div_texts

if __name__ == "__main__":
    url = "https://www.bcc.kz/personal/cards_copy"  # Replace with your URL
    
    card_name_candidates = parse_div_text_by_class(url, "heading-2")
    cashback_candidates = parse_div_text_by_class(url, "title-text") # some values might be not relevant

    # Extract names using regular expression
    card_names = []
    for candidate in card_name_candidates:
        #text = div.inner_text()
        match = re.findall(r'#\w+', candidate)
        if match:
            #name = match.group(1)
            card_names.append(candidate)

    # Extract percent values using regular expression
    cashbacks = []
    for candidate in cashback_candidates:
        #text = div.inner_text()
        match = re.search(r'(\d+)%', candidate)
        if match:
            percent_value = match.group(1)
            cashbacks.append(percent_value)

    ##################################
    ##store in data base
    ##################################
    print(card_names)
    print(cashbacks)
