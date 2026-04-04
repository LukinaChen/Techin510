# This app is a GIX Campus Wayfinder built with Streamlit.
# It helps new GIX students find campus resources by searching
# and filtering by category.

import streamlit as st

# Data integrity check
REQUIRED_FIELDS = {"name", "category", "location", "hours", "description", "free"}

RESOURCES = [
    {
        "name": "GIX Makerspace",
        "category": "Makerspace",
        "location": "Floor 1, GIX Building",
        "hours": "Mon-Fri 8am-10pm, Sat-Sun 10am-6pm",
        "description": "Fully equipped makerspace with 3D printers, laser cutters, and electronics tools.",
        "free": True,
    },
    {
        "name": "Free Printing Station",
        "category": "Printing",
        "location": "Floor 2, near elevator",
        "hours": "Mon-Fri 8am-8pm",
        "description": "Free black and white printing for GIX students. Color printing available at cost.",
        "free": True,
    },
    {
        "name": "Bike Storage Room",
        "category": "Storage",
        "location": "Basement, GIX Building",
        "hours": "24/7",
        "description": "Secure bike storage for GIX students. Requires student ID for access.",
        "free": True,
    },
    {
        "name": "Quiet Study Room A",
        "category": "Study Space",
        "location": "Floor 3, Room 301",
        "hours": "Mon-Fri 7am-11pm",
        "description": "Silent study room with individual desks and natural lighting.",
        "free": True,
    },
    {
        "name": "Collaborative Study Lounge",
        "category": "Study Space",
        "location": "Floor 2, open area",
        "hours": "Mon-Sun 7am-midnight",
        "description": "Open lounge with whiteboards and group tables for team collaboration.",
        "free": True,
    },
    {
        "name": "Campus Cafe",
        "category": "Food",
        "location": "Floor 1, main entrance",
        "hours": "Mon-Fri 7:30am-4pm",
        "description": "Coffee, tea, and light snacks. Student discount available with ID.",
        "free": False,
    },
    {
        "name": "Locker Storage",
        "category": "Storage",
        "location": "Floor 1, near gym",
        "hours": "24/7",
        "description": "Day-use lockers for storing personal belongings on campus.",
        "free": True,
    },
    {
        "name": "VR/AR Lab",
        "category": "Makerspace",
        "location": "Floor 2, Room 205",
        "hours": "Mon-Fri 9am-6pm",
        "description": "VR and AR equipment available for student projects. Booking required.",
        "free": True,
    },
]

# Assert data integrity
assert all(
    REQUIRED_FIELDS.issubset(r.keys()) for r in RESOURCES
), "Some resources are missing required fields!"

def main():
    st.set_page_config(page_title="GIX Campus Wayfinder", layout="wide")
    st.title("GIX Campus Wayfinder")
    st.write("Find campus resources at GIX. Search or filter by category below.")

    # Sidebar filter
    st.sidebar.header("Filter by Category")
    categories = ["All"] + sorted(set(r["category"] for r in RESOURCES))
    selected_category = st.sidebar.selectbox("Category", categories)

    # Search bar with button
    st.header("Search Resources")
    col_search, col_btn = st.columns([4, 1])
    with col_search:
        search = st.text_input(
            "Search",
            placeholder="e.g. printing, bike, study...",
            label_visibility="collapsed"
        )
    with col_btn:
        search_clicked = st.button("🔍 Search")

    # Filter logic
    filtered = RESOURCES
    if selected_category != "All":
        filtered = [r for r in filtered if r["category"] == selected_category]
    if search or search_clicked:
        filtered = [
            r for r in filtered
            if search.lower() in r["name"].lower()
            or search.lower() in r["description"].lower()
        ]

    # Display results
    st.header(f"Results ({len(filtered)} found)")

    if not filtered:
        st.warning("No resources match your search. Try a different keyword or category.")
    else:
        for resource in filtered:
            with st.container():
                st.subheader(resource["name"])
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Category:** {resource['category']}")
                    st.write(f"**Location:** {resource['location']}")
                    st.write(f"**Hours:** {resource['hours']}")
                with col2:
                    st.write(f"**Description:** {resource['description']}")
                    st.write(f"**Free to use:** {'Yes' if resource['free'] else 'No'}")
                st.divider()

if __name__ == "__main__":
    main()
    