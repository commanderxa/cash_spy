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
    
def get_links_from_buttons(url, button_class):
    # Launch the browser
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        buttons = page.query_selector_all(button_class)
        links = [button.get_attribute('href') for button in buttons]

        return links 
    

def get_a_href(url, class_name):
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
        page.wait_for_selector(f'a.{class_name}')
        
        # Get all divs with the specified class name
        a_s = page.query_selector_all(f'a.{class_name}')
        #print(a_s)
        links = [a.get_attribute('href') for a in a_s]
        
        # Close the browser
        browser.close()
        
        return links


if __name__ == "__main__":
    # url = "https://www.bcc.kz/personal/cards_copy"  # Replace with your URL
    
    # card_name_candidates = parse_div_text_by_class(url, "heading-2")
    # cashback_candidates = parse_div_text_by_class(url, "title-text") # some values might be not relevant

    # # Extract names using regular expression
    # card_names = []
    # for candidate in card_name_candidates:
    #     #text = div.inner_text()
    #     match = re.findall(r'#\w+', candidate)
    #     if match:
    #         #name = match.group(1)
    #         card_names.append(candidate)

    # # Extract percent values using regular expression
    # cashbacks = []
    # for candidate in cashback_candidates:
    #     #text = div.inner_text()
    #     match = re.search(r'(\d+)%', candidate)
    #     if match:
    #         percent_value = match.group(1)
    #         cashbacks.append(percent_value)

    # ##################################
    # ##store in data base
    # ##################################
    # print(card_names)
    # print(cashbacks)

    ''' Part to get partners for card type(3)'''

    links = get_a_href('https://club.bcc.kz/?city=21', 'card-select')


    for link in links:
        print("Card type:" + link[1:])
        card_partners_link = 'https://club.bcc.kz' + link
        partners = parse_div_text_by_class(card_partners_link, 'text-info h2')
        partner_cashbacks = parse_div_text_by_class(card_partners_link, 'installment')
        #print(partners)
        print(partner_cashbacks)

    


