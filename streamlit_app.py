import streamlit as st
import pandas as pd
from scraper import collect_data


# List of food items
food_items = [
    "lean beef cuts", "ground pork", "ground turkey", "ground chicken", "ground lean beef", 
    "chicken thigh", "chicken breast", "pork tenderloin", "canned tuna", "canned chicken", 
    "deli turkey", "deli ham", "salmon", "shrimp frozen", "tofu", "eggs", "black beans", 
    "pinto beans", "refried beans", "lentils", "almonds", "peanuts", "cashews", "pumpkin seeds", 
    "sunflower seeds", "protein powder", "brown rice", "white rice", "quinoa", "sourdough bread", 
    "whole grain bread", "wheat bread", "corn tortillas", "flour tortillas", "pasta", 
    "whole wheat bagels", "pita", "naan", "whole grain cereals", "whole grain pancake mix", 
    "oatmeal", "potatoes", "sweet potatoes", "butter", "olive oil", "canola oil", "bananas", 
    "blueberries", "strawberries", "blackberries", "oranges", "apples", "grapes", "pineapple", 
    "watermelon", "cantaloupe", "kale", "romaine", "salad mix", "spinach", "collard greens", 
    "corn", "tomatoes", "edamame", "beets", "avocado", "green beans", "broccoli", "cauliflower", 
    "mushrooms", "lemons", "limes", "red bell peppers", "green bell peppers", "cucumbers", 
    "carrots", "squash", "onions", "garlic", "guajillo chiles", "árbol chiles", "ancho chiles", 
    "chipotles", "jalapeno", "whole milk", "2% milk", "soy milk", "almond milk", "oat milk", 
    "greek yogurt", "creamer", "cottage cheese", "cheese", "peanut butter", "almond butter", 
    "low sugar jelly", "canned tomatoes", "canned peas", "canned corn", "canned jalapenos", 
    "canned soup", "healthy salad dressing", "salsa", "pasta sauce", "pesto", "frozen veggies", 
    "frozen breakfast burritos", "frozen lasagna", "ketchup", "mustard", "mayo", "sriracha", 
    "mac and cheese", "tea", "coffee", "salt", "pepper", "garlic powder", "tajin", "cinnamon", 
    "vitamins", "men’s vitamins", "women’s vitamins", "prenatal vitamins", "children vitamins", 
    "baby diapers", "baby formula", "baby wipes", "baby food", "pads", "tampons", "laundry soap", 
    "dish soap", "dishwasher soap", "toilet paper", "paper towels", "sponges", "batteries"
]

def main():
    st.title("Grocery Price Tracker")
    st.write("Track the prices of various food items from different grocery stores.")
    
    selected_item = st.selectbox("Search for a food item", sorted(food_items))
    if st.button("Update Prices"):
        data = collect_data(selected_item)
        st.session_state['data'] = data
    else:
        if 'data' not in st.session_state:
            st.write("Click the button to update prices.")
        else:
            data = st.session_state['data']
    
    if 'data' in st.session_state:
        data = st.session_state['data']
        
        # Convert the data to a DataFrame
        df = pd.DataFrame(data, columns=["title", "price", "store"])
        
        # Ensure 'title' column is of type str
        df['title'] = df['title'].astype(str)
        
        # Filter data based on selected item
        filtered_data = df[df['title'].str.contains(selected_item, case=False, na='')]
        
        st.dataframe(filtered_data)

        if not filtered_data.empty:
            # Convert 'price' to numeric, errors='coerce' will turn non-numeric values into NaN
            filtered_data['price'] = pd.to_numeric(filtered_data['price'], errors='coerce')
            
            # Group by 'store' to get average price per store (or use other aggregation if needed)
            price_by_store = filtered_data.groupby('store')['price'].mean().reset_index()
            
            # Create a bar chart
            st.bar_chart(price_by_store.set_index('store'))

        else:
            st.write("No data available for the selected item.")


if __name__ == "__main__":
    main()

