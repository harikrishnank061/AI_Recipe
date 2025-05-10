import streamlit as st
import cohere
import time

# Function to generate cooking recipe using Cohere Chat API
def generate_recipe(api_key, ingredients, cuisine="general", complexity="easy"):
    try:
        # Initialize the Cohere client with the provided API key
        co = cohere.Client(api_key)
        
        # Create the prompt message for the chat API
        prompt = f"Create a {complexity} {cuisine} recipe using these ingredients: {ingredients}."
        
        # Call the chat method from Cohere API with a reduced max_tokens to speed up the response
        response = co.chat(
            model="command-xlarge-nightly",
            message=prompt,
            max_tokens=200,  # Reduced tokens for quicker responses
            temperature=0.7,
            p=0.75,
            stop_sequences=["\n"],
            frequency_penalty=0.2,
            presence_penalty=0.2
        )
        
        # Return the generated recipe
        return response.reply.strip()
    except Exception as e:
        # Handle errors and display error messages in the Streamlit app
        st.error(f"Error: {str(e)}")
        return None

# Streamlit app layout
st.set_page_config(page_title="Cooking Recipe Generator", page_icon="🥘")
st.title("🥘 Cooking Recipe Generator")
st.markdown("Generate cooking recipes based on the ingredients you have.")

# Input API key directly in the app
api_key = st.text_input("Enter your Cohere API Key", type="password")

# Show a warning if the API key is not provided
if not api_key:
    st.warning("⚠️ Please enter your Cohere API key to proceed.")

# Input fields for recipe generation
ingredients = st.text_area("Enter the ingredients you have (comma-separated)", height=150)
cuisine = st.selectbox("Cuisine Type", ["general", "Italian", "Chinese", "Mexican", "Indian", "Mediterranean", "French"], index=0)
complexity = st.selectbox("Recipe Complexity", ["easy", "medium", "complex"], index=0)

# Button to trigger recipe generation
if st.button("Generate Recipe"):
    if api_key and ingredients.strip():
        # Add a loading spinner while generating the recipe
        with st.spinner("Generating recipe... Please wait."):
            start_time = time.time()
            recipe = generate_recipe(api_key, ingredients, cuisine=cuisine, complexity=complexity)
            end_time = time.time()
            if recipe:
                st.subheader("Generated Recipe:")
                st.write(recipe)
            st.write(f"Recipe generated in {end_time - start_time:.2f} seconds.")
    else:
        st.warning("⚠️ Please provide both the API key and the ingredients to generate a recipe.")

st.markdown("---")
st.caption("Powered by Cohere | Built with ❤️ using Streamlit")
