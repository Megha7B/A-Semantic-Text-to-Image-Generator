import streamlit as st
import os
from PIL import Image
from image_generator import ImageGenerator
from config import Config

# Set page configuration
st.set_page_config(
    page_title="Semantic Text-to-Image Generator",
    page_icon="🎨",
    layout="wide"
)

# Initialize the image generator
@st.cache_resource
def get_image_generator():
    return ImageGenerator()

def main():
    # Set up the UI
    st.title("🎨 Semantic Text-to-Image Generator")
    st.write("Generate images from text descriptions using semantic understanding")
    
    # Create tabs for different modes
    tab1, tab2 = st.tabs(["Text to Image", "Image Variation"])
    
    # Text to Image tab
    with tab1:
        st.header("Generate Image from Text")
        
        # Text input
        prompt = st.text_area("Enter your text description:", height=100)
        
        # Generation parameters
        col1, col2 = st.columns(2)
        with col1:
            num_images = st.slider("Number of images to generate:", 1, 4, 1)
        with col2:
            inference_steps = st.slider("Inference steps:", 10, 50, Config.NUM_INFERENCE_STEPS)
            Config.NUM_INFERENCE_STEPS = inference_steps
        
        # Generate button
        if st.button("Generate Images", key="gen_btn"):
            if prompt:
                with st.spinner("Generating images..."):
                    try:
                        generator = get_image_generator()
                        image_paths = generator.generate_image(prompt, num_images)
                        
                        # Display the generated images
                        st.subheader("Generated Images:")
                        image_cols = st.columns(min(num_images, 4))
                        
                        for i, path in enumerate(image_paths):
                            with image_cols[i % 4]:
                                img = Image.open(path)
                                st.image(img, caption=f"Image {i+1}", use_column_width=True)
                                st.write(f"Saved at: {path}")
                    except Exception as e:
                        st.error(f"Error generating images: {str(e)}")
            else:
                st.warning("Please enter a text description")
    
    # Image Variation tab
    with tab2:
        st.header("Generate Variations of an Image")
        
        # Upload image
        uploaded_file = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])
        
        if uploaded_file is not None:
            # Display the uploaded image
            st.subheader("Uploaded Image:")
            img = Image.open(uploaded_file)
            st.image(img, width=256)
            
            # Save the uploaded image
            temp_path = os.path.join("temp", uploaded_file.name)
            os.makedirs("temp", exist_ok=True)
            img.save(temp_path)
            
            # Text input
            variation_prompt = st.text_area("Enter a description for the variation:", height=100, key="var_prompt")
            
            # Generation parameters
            col1, col2, col3 = st.columns(3)
            with col1:
                num_variations = st.slider("Number of variations:", 1, 4, 1)
            with col2:
                strength = st.slider("Variation strength:", 0.1, 1.0, 0.75, 0.05)
            with col3:
                var_steps = st.slider("Inference steps:", 10, 50, Config.NUM_INFERENCE_STEPS, key="var_steps")
            
            # Generate button
            if st.button("Generate Variations", key="var_btn"):
                if variation_prompt:
                    with st.spinner("Generating variations..."):
                        try:
                            # Create a custom generator for variations
                            generator = get_image_generator()
                            # Set strength for this generation
                            generator.variation_strength = strength
                            # Set steps
                            Config.NUM_INFERENCE_STEPS = var_steps
                            
                            # Generate variations
                            variation_paths = generator.generate_variations(
                                temp_path, 
                                variation_prompt, 
                                num_variations
                            )
                            
                            # Display the generated variations
                            st.subheader("Generated Variations:")
                            var_cols = st.columns(min(num_variations, 4))
                            
                            for i, path in enumerate(variation_paths):
                                with var_cols[i % 4]:
                                    var_img = Image.open(path)
                                    st.image(var_img, caption=f"Variation {i+1}", use_column_width=True)
                                    st.write(f"Saved at: {path}")
                        except Exception as e:
                            st.error(f"Error generating variations: {str(e)}")
                else:
                    st.warning("Please enter a description for the variation")

if __name__ == "__main__":
    main() 