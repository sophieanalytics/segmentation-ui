import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle 
import squarify 
from streamlit_option_menu import option_menu
import pyarrow

st.set_page_config(
    page_title='Customer Segmentation',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.title("🧠 Customer Segmentation System")
menu = ["Project Overview", "Segmentation App" ]

# choice = st.sidebar.radio('MENU', menu)

# Sidebar menu
with st.sidebar:
    choice = option_menu(
        menu_title=None,  # No title
        options=["Project Overview", "Segmentation App"],
        # icons=["house", "bi bi-bar-chart", "list-task", "search", "info-circle"],
        icons = ['house', 'list-task'],
        default_index=0,  # Default to "Kết Quả"
        orientation="vertical",
        styles={
            "container": {"padding": "10px", "background-color": "#0f0f0f", "border-radius": "10px"},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "color": "#fff",
                "padding": "10px 15px",
                "border-radius": "6px"
            },
            "nav-link-selected": {
                "background-color": "#FF4B4B",  # This is the red highlight
                "color": "white"
            }
        }
    )
    
# Footer
st.sidebar.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 16px; line-height: 1.5;'>
        Made by <b>Tran T. Kim Phung & Ta Van Hoang</b><br>
        Instructed by <b>Khuat Thuy Phuong</b> ❤️ <br>
        April 2025
    </div>
    """,
    unsafe_allow_html=True
)

if choice == 'Project Overview':
    st.markdown("""
            We are developing a **Customer Segmentation System** designed to empower businesses with data-driven insights into their customer base.

            By leveraging data provided by the store—such as purchase history, frequency, demographics, and engagement patterns—our system identifies **distinct customer groups** through advanced segmentation techniques.

            With this powerful insight, businesses can:

            - 🎯 **Tailor marketing strategies** to specific customer personas  
            - 🛍️ **Optimize product offerings** to match customer needs  
            - 💬 **Enhance customer care** through personalized experiences  
            - 🔁 **Improve retention and loyalty** by understanding behavioral patterns  

            This system transforms raw customer data into **actionable strategies**, enabling **smarter decisions** and **sustainable growth**.
            """)
    
    tab1, tab2, tab3 = st.tabs(['Methodology', 'Data Exploration', 'Kmeans Model'])
    
    with tab1:
        st.subheader('Methodology')
        st.image('image/methodology.jpg')
    
    with tab2:
        st.subheader('Dataset')
        st.image('image/2025-04-11 19.06.55.jpg')
        
        st.subheader('Charts')
        st.image('image/explore1.jpg')
        st.image('image/explore2.jpg')
        st.image('image/explore3.jpg')
    
    with tab3:
        st.subheader('KMeans Clustering')
        st.markdown("""
            KMeans is an unsupervised machine learning algorithm used to automatically group similar data points into distinct clusters.
            
            In the context of customer segmentation, KMeans helps businesses:
            - Discover hidden customer groups based on behavior and demographics
            - Understand which features (e.g., spending, frequency) define each group
            - Personalize marketing and services by targeting each segment effectively 
               
                """)
        st.markdown('With this dataset, the optimal number of clusters appears to be 5, since that''s where the elbow is most pronounced.')
        st.image('image/2025-04-11 19.06.50.jpg')
    
        st.markdown("""
                This bubble chart highlights key customer groups based on how recently they purchased and how much they tend to spend
                """)
        st.image('image/2025-04-11 19.06.35.jpg')

        st.markdown("""
            ### ✅ Segmentation Complete!

            The model has been successfully trained and has identified **5 distinct customer groups** based on purchasing behavior.

            ---

            📊 These groups include:  
            - **VIP**  
            - **Active**  
            - **Potential**  
            - **Inactive**  
            - **Lost**

            ---

            🔄 Now it’s time to **experience the product** by inputting new data with 3 required columns:

            - **R** – Recency: Number of days since the last purchase  
            - **F** – Frequency: Number of purchases  
            - **M** – Monetary: Total amount spent

            ---

            👉 Please proceed to the **next section** to upload your data and discover which segment your customers belong to!
            """)


    
elif choice == 'Segmentation App':
    st.subheader('Welcome to our product — we invite you to explore and enjoy the experience!')
    # add image
    st.image('https://www.marketingevolution.com/hs-fs/hubfs/customer-segmentation.jpg?width=1100&name=customer-segmentation.jpg')
    
    # data methods
    st.markdown('## First, Please choose how to provide data: ')

    if "manual_data" not in st.session_state:
        st.session_state["manual_data"] = []
    
    df = None
    input_method = st.radio('Input method', ['Enter data manually', 'Upload CSV file'])
    
    if input_method == 'Upload CSV file':
        st.markdown('##### Please try with sample data or provide a CSV file that includes the following columns: Recency, Frequency, and Monetary')
         # dropdown with sample data
        sample_option = st.selectbox("Choose a sample dataset:", ["None", "Sample"])
        # upload csv
        uploaded_csv = st.file_uploader('Upload a CSV file', type = ['csv'])

        
        # Sample datasets
        sample_1 = pd.DataFrame({
            'Recency':   [10, 45, 3, 90, 25, 100,200,300,130,200,90, 25, 0,0],
            'Frequency': [5, 1, 10, 2, 3, 10,2,5,10,30,50,60, 10,3],
            'Monetary': [500, 100, 1000, 150, 300, 50,20,30,10,40,200,600,10, 200]
        })
        
        if uploaded_csv is not None:
            df = pd.read_csv(uploaded_csv)
        elif sample_option == "Sample":
            df = sample_1     

        if df is not None: 
            try:
                st.subheader('Result:')
                #load csv
                # df = pd.read_csv(uploaded_csv)
                st.success('File uploaded successfully!')
            except Exception as e:
                st.error(f'error reading file: {e}')
                
    elif input_method == 'Enter data manually':
        st.markdown('#### Manual Data Entry')
        with st.form('manual_form'):
            recency = st.number_input('Recency', min_value = 0, step = 1)
            frequency = st.number_input('Frequency', min_value = 1, step = 1)
            monetary = st.number_input('Monetary', min_value = 0.0, step = 0.01)
            # submit button
            submitted = st.form_submit_button('➕ Add Entry')
        
        if submitted:
            st.session_state['manual_data'].append({
                'Recency': recency,
                'Frequency': frequency,
                'Monetary': monetary
            })
            st.success('Entry added!')
            
        if st.session_state['manual_data']:
            df = pd.DataFrame(st.session_state['manual_data'])
            st.subheader('Current entries')
            st.dataframe(df)
            
            if st.button('Clear manual entries'):
                st.session_state['manual_data'] = []
                st.success('Manual data cleared')
    
    if (input_method == "Upload CSV file" and df is not None) or \
        (input_method == "Enter data manually" and st.session_state["manual_data"]):
        st.markdown('## Now, you can start running segmentation by clicking button as below: ')
        if st.button('Run segmentation'):    
            if df is not None: 
                try:    
                    # upload model
                    with open('kmeans_model.pkl', 'rb') as f:
                        loaded_model = pickle.load(f)
                    
                    # only show summary table if entries > 50
                    if len(df) > 50:
                        # show summary
                        st.subheader('Descriptive statistics')
                        st.markdown(
                        df.describe().round(2).to_html(classes='big-table', index=True),
                        unsafe_allow_html=True
                        )

                    # Predict new data
                    prediction = loaded_model.predict(df)
                    df['Cluster'] = prediction
                    
                    cluster_names = {
                        0: 'POTENTIAL',     # Không hoạt động lâu (192 ngày), giá trị trung bình (78)
                        1: 'ACTIVE',        # Hoạt động gần đây nhất (55 ngày), giá trị ổn định (71)
                        2: 'VIP',           # Hoạt động gần (64 ngày), tần suất cao (17), giá trị cao (175)
                        3: 'LOST',          # Không hoạt động rất lâu (560 ngày), giá trị thấp (37)
                        4: 'INACTIVE'       # Không hoạt động lâu (353 ngày), giá trị thấp (61)
                    }

                    # DRAW CHARTS
                    rfm_agg = df.groupby('Cluster').agg({
                        'Recency': 'mean',
                        'Frequency': 'mean',
                        'Monetary': ['mean', 'count']}).round(0)
                    rfm_agg.columns = rfm_agg.columns.droplevel()
                    rfm_agg.columns = ['RecencyMean','FrequencyMean','MonetaryMean', 'Count']
                    rfm_agg['Percent'] = round((rfm_agg['Count']/rfm_agg.Count.sum())*100, 2)
                    rfm_agg = rfm_agg.reset_index()
                    rfm_agg['Cluster'] = rfm_agg['Cluster'].map(cluster_names)
                    
                    st.subheader(f'We have segmented the data into {rfm_agg.index.max()+1} distinct groups')
                    st.dataframe(rfm_agg)
                    
                    fig, ax = plt.subplots(figsize=(10,10))
                    
                    # Define color mapping
                    colors_dict2 = {'POTENTIAL':'yellow','ACTIVE':'royalblue', 'VIP':'cyan',
                                'LOST':'red', 'INACTIVE':'purple'}
                    
                    squarify.plot(
                        sizes=rfm_agg['Count'],
                        text_kwargs={'fontsize':12,'weight':'bold', 'fontname':"sans serif"},
                        color=colors_dict2.values(),
                        label=[f"{i} \n{dd} days  \n{o:.0f} orders \n{m}$ \n {c} customers ({p}%)" 
                            for i, dd, o, m ,c ,  p  in zip(rfm_agg['Cluster'], rfm_agg['RecencyMean'], rfm_agg['FrequencyMean'], 
                                                        rfm_agg['MonetaryMean'], rfm_agg['Count'], rfm_agg['Percent']
                                                    )],
                        alpha=0.8,
                        ax=ax
                    )
                    st.pyplot(fig)
                    
                except Exception as e:
                    st.error(f'error reading file: {e}')
                    
            else: 
                st.warning('No data. Please provide data before running segmentation')   
        
    