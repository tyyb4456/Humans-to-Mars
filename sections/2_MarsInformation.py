import streamlit as st
import random

def load_mars_facts():
    return [
        "Mars has the largest volcano in the solar system, Olympus Mons.",
        "Mars has two moons: Phobos and Deimos.",
        "A year on Mars is 687 Earth days long.",
        "Mars' atmosphere is 95% carbon dioxide.",
        "Mars has the largest dust storms in the solar system.",
        "The average temperature on Mars is about -63°C (-82°F).",
        "Mars' gravity is about 38% of Earth's.",
        "Sunsets on Mars appear blue due to the way dust scatters light.",
        "Mars has seasons like Earth because both planets are tilted on their axes.",
        "The highest mountain on Mars is three times taller than Mount Everest."
    ]

def main():
    st.title("Mars Information Center")
    
    # Tabs for different categories
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Geography", "Missions", "Research"])
    
    with tab1:
        st.header("About Mars")
        st.write("""
        Mars, often called the Red Planet, is the fourth planet from the Sun in our solar system. 
        It has captured human imagination for centuries and is a prime target for space exploration.
        
        The planet's reddish appearance is due to iron oxide (rust) on its surface. Mars has many 
        Earth-like features including polar ice caps, seasons, and a day length similar to Earth's.
        """)
        
        # Did You Know widget
        with st.expander("Did You Know? (Click to reveal a random fact)"):
            fact = random.choice(load_mars_facts())
            st.info(fact)
    
    with tab2:
        st.header("Martian Geography")
        st.write("""
        Mars features some of the most dramatic landscapes in the solar system:
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Major Features")
            st.write("""
            - **Olympus Mons**: The largest volcano in the solar system
            - **Valles Marineris**: A canyon system as long as the United States
            - **Polar Ice Caps**: Composed of water ice and dry ice
            - **Impact Craters**: Including the massive Hellas Basin
            """)
        
        with col2:
            st.image("https://api.nasa.gov/assets/img/general/mars_valley.jpg", 
                    caption="Valles Marineris on Mars",
                    use_container_width=True)
    
    with tab3:
        st.header("Mars Missions")
        st.write("""
        Numerous missions have been sent to Mars, including rovers, landers, and orbiters.
        Here are some of the most significant ongoing missions:
        """)
        
        # Mission timeline
        with st.expander("Active Missions"):
            st.write("🚀 **Perseverance Rover (2020-present)**")
            st.write("- Searching for signs of ancient microbial life")
            st.write("- Collecting rock and soil samples")
            st.write("- Testing oxygen production from Mars atmosphere")
            
            st.write("🚀 **Curiosity Rover (2012-present)**")
            st.write("- Studying Mars' climate and geology")
            st.write("- Assessing environmental conditions for microbial life")
            
            st.write("🚀 **InSight Lander (2018-present)**")
            st.write("- Studying Mars' interior structure")
            st.write("- Measuring Marsquakes")
    
    with tab4:
        st.header("Current Research")
        st.write("""
        Scientists are currently focusing on several key areas of Mars research:
        """)
        
        research_areas = {
            "Search for Life": "Investigating potential biosignatures and habitable environments",
            "Climate Studies": "Understanding Mars' past and present climate patterns",
            "Human Exploration": "Preparing for future human missions to Mars",
            "Geological History": "Mapping the planet's geological evolution"
        }
        
        for area, description in research_areas.items():
            with st.expander(area):
                st.write(description)

if __name__ == "__main__":
    main()