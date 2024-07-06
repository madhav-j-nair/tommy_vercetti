from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st

# Function to scrape mission or character data
def scrape_data(web):
    driver = webdriver.Edge()
    data = []

    try:
        driver.get(web)

        # Wait for the content to load (adjust timeout as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'wikitable'))
        )

        # Find all elements with class 'wikitable' (assuming each table is a mission or character list)
        tables = driver.find_elements(By.CLASS_NAME, 'wikitable')

        data.append(("Title", "Description", "Rewards"))

        # Process each table
        for table in tables:
            rows = table.find_elements(By.TAG_NAME, 'tr')

            for row in rows[1:]:  # Start from index 1 to skip the header row
                cells = row.find_elements(By.TAG_NAME, 'td')

                # Extracting data based on number of cells
                if len(cells) >= 3:
                    title = cells[0].text.strip()
                    description = cells[1].text.strip()
                    rewards = cells[2].text.strip()
                elif len(cells) == 2:
                    title = cells[0].text.strip()
                    description = cells[1].text.strip()
                    rewards = "N/A"
                elif len(cells) == 1:
                    title = cells[0].text.strip()
                    description = "N/A"
                    rewards = "N/A"
                else:
                    title = "N/A"
                    description = "N/A"
                    rewards = "N/A"

                data.append((title, description, rewards))

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

    return data

# Main Streamlit app code
def main():
    options = {
        'GTA V - Missions': ("https://gta.fandom.com/wiki/Missions_in_GTA_V", "https://gta-5-map.com?x=-163.6523437500003&y=71.77394078102989&zoom=3"),
        'GTA V - Characters': ("https://gta.fandom.com/wiki/Characters_in_GTA_V", "https://gta-5-map.com?x=-163.6523437500003&y=71.77394078102989&zoom=3"),
        'GTA IV - Missions': ("https://gta.fandom.com/wiki/Missions_in_GTA_IV", "https://mapgenie.io/grand-theft-auto-4/maps/liberty-city?x=-0.987455216445511&y=0.9346968200040919&zoom=10"),
        'GTA IV - Characters': ("https://gta.fandom.com/wiki/Characters_in_GTA_IV", "https://mapgenie.io/grand-theft-auto-4/maps/liberty-city?x=-0.987455216445511&y=0.9346968200040919&zoom=10"),
        'GTA San Andreas - Missions': ("https://gta.fandom.com/wiki/Missions_in_GTA_San_Andreas", "https://mapgenie.io/grand-theft-auto-san-andreas/maps/san-andreas"),
        'GTA San Andreas - Characters': ("https://gta.fandom.com/wiki/Characters_in_GTA_San_Andreas", "https://mapgenie.io/grand-theft-auto-san-andreas/maps/san-andreas"),
        'GTA Vice City - Missions': ("https://gta.fandom.com/wiki/Missions_in_GTA_Vice_City", "https://mapgenie.io/grand-theft-auto-vice-city/maps/vice-city"),
        'GTA Vice City - Characters': ("https://gta.fandom.com/wiki/Characters_in_GTA_Vice_City", "https://mapgenie.io/grand-theft-auto-vice-city/maps/vice-city"),
        'GTA III - Missions': ("https://gta.fandom.com/wiki/Missions_in_GTA_III", "https://mapgenie.io/grand-theft-auto-3/maps/liberty-city?x=-0.9846496582034376&y=0.7815512159524047&zoom=10"),
        'GTA III - Characters': ("https://gta.fandom.com/wiki/Characters_in_GTA_III", "https://mapgenie.io/grand-theft-auto-3/maps/liberty-city?x=-0.9846496582034376&y=0.7815512159524047&zoom=10")
    }
    st.image("maxresdefault.jpg")
    st.title('GTA GUIDE')
    n = st.selectbox('Choose a GTA Game and Category', list(options.keys()))

    selected_value = options.get(n)

    if selected_value:
        mission_data = scrape_data(selected_value[0])
        character_data = []

        if selected_value[1]:
            st.markdown(f"### {n.split(' - ')[0]} Map")
            st.components.v1.iframe(selected_value[1])

        st.markdown(f"### {n}")
        if mission_data:
            st.table(mission_data)
        else:
            st.write("No data found. Please check the website or try again later.")

if __name__ == '__main__':
    main()
