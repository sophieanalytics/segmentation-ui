import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle 
import squarify 

st.set_page_config(
    page_title='Customer Segmentation',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.title("Customer Segmentation")
menu = ["Segmentation App", "Project Overview"]
choice = st.sidebar.radio('Menu', menu)



if choice == 'Project Overview':
    st.subheader('Tran Thi Kim Phung & Ta Van Hoang')
elif choice == 'Segmentation App':
    st.subheader('Welcome to our product — we invite you to explore and enjoy the experience!')
    # add image
    st.image('https://www.marketingevolution.com/hs-fs/hubfs/customer-segmentation.jpg?width=1100&name=customer-segmentation.jpg')
    
    # data methods
    st.markdown('## First, Please choose how to provide data: ')
    
    if "manual_data" not in st.session_state:
        st.session_state["manual_data"] = []
    
    df = None
    input_method = st.radio('Input method', ['Upload CSV file', 'Enter data manually'])
    
    if input_method == 'Upload CSV file':
        st.markdown('##### Please provide a CSV file that includes the following columns: Recency, Frequency, and Monetary')
        uploaded_csv = st.file_uploader('Upload a CSV file', type = ['csv'])
        if uploaded_csv is not None: 
            try:
                st.subheader('Result:')
                #load csv
                df = pd.read_csv(uploaded_csv)
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
    
    if (input_method == "Upload CSV file" and uploaded_csv is not None) or \
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
        
    