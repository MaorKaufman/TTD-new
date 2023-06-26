import streamlit as st
import requests
import json

def intro():
    pass
#-------------------------------Drop down options-----------------------------------
###------------------------------Get counts func------------------------------------
def get_counts(): 
    if demo_name == "Get Counts":
        st.subheader("Get segment count API")
        segID = st.text_input("Please insert SegmentID: ")
        auth = get_authentication_token()
        
        if auth is not None:
            API_URL = "https://api.thetradedesk.com/v3/thirdpartydata/query"
            headers = {
                "TTD-Auth": auth,
                "Content-Type": "application/json"
            }
            data = {
                "ProviderId": "startapp",
                "ProviderElementId": segID,
                "IncludeActiveIDsCountExpandedFlag": "true",
                "PageStartIndex": "0",
                "PageSize": "100"
            }
            response = requests.post(url=API_URL, headers=headers, json=data)
            
            if response.status_code >= 200 and response.status_code < 300 and response.json()['ResultCount'] != 0:
                result = response.json()
                st.table(result['Result'][0])
            else:
                st.write("Could not retrieve data. Please note that SegmentID must be greater than 0 and valid.")
        else:
            st.write("Error: Could not retrieve Token from TTD.")
    else:
        clear_inputs()
###------------------------------Update segment name------------------------------------
def update_segment_name():
    if demo_name == "Update segment name":
        st.subheader("Update segment name and/or description API")
        segID = st.text_input("Please insert SegmentID: ")
        newSegName = st.text_input("Please insert the new segment name: ")
        newDescription = st.text_input("Please insert the new description: ")
        
        auth = get_authentication_token()
        
        if auth is not None:
            API_URL = "https://api.thetradedesk.com/v3/thirdpartydata"
            headers = {
                "TTD-Auth": auth,
                "Content-Type": "application/json"
            }
            payload = {
                "ProviderId": "startapp",
                "ProviderElementId": segID,
                "ParentElementId": "customstartapp",
                "DisplayName": newSegName,
                "Buyable": 1,
                "Description": newDescription
            }
            
            if newSegName != "" and newDescription != "" and segID != "":
                response = requests.put(url=API_URL, headers=headers, json=payload)
                
                if response.status_code >= 200 and response.status_code < 300:
                    result = response.json()
                    st.subheader("Segment name and/or description updated successfully")
                    st.table(result)
                else:
                    st.write("Request was not successful.")
            else:
                st.write("Please insert all mandatory fields.")
        else:
            st.write("Error: Could not retrieve Token from TTD.")
    else:
        clear_inputs()
###------------------------------Update partnerID/CPM/POM------------------------------------        
def update_partnerID_CPM_POM():
    if demo_name == "Update partnerID or CPM/POM":
        st.subheader("Update partnerID/CPM/POM tool")
       #  st.write("Please fill all the details")
        segID = st.text_input("Please insert SegmentID: ")
        PartnerID = st.text_input("Please insert PartnerID: ")
        CappedCPM = st.text_input("Please insert Capped CPM: ")
        POM = st.text_input("Please insert percentage of media: ")
        Activator_email = st.text_input("Please insert the activator Email address: ")
        
###------------------------------get token------------------------------------        
def get_authentication_token():
    API_URL = "https://api.thetradedesk.com/v3/authentication"
    data = {
        "Login": "ttd_api_startapp@startapp.com",
        "Password": "sodaCSM2019!",
        "TokenExpirationInMinutes": 1440.0
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url=API_URL, headers=headers, json=data)
    
    if response.status_code >= 200 and response.status_code < 300:
        data = response.json()
        return data['Token']
    else:
        return None
###------------------------------clear------------------------------------        
def clear_inputs():
    st.text_input("Please insert SegmentID: ", value="")
    st.text_input("Please insert the new segment name: ", value="")
    st.text_input("Please insert the new description: ", value="")
#####------------------------------clear------------------------------------        
page_names_to_funcs = {
    "—": intro,
    "Get Counts": get_counts,
    "Update segment name": update_segment_name,
    "Update partnerID or CPM/POM" : update_partnerID_CPM_POM
}

st.sidebar.title("Welcome to Start.io's TTD's UI tool")
st.sidebar.subheader("This tool was created to enable Start.io's team to get details/update custom/prepack segments on TTD's side.")

demo_name = st.sidebar.selectbox("Choose a UI", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
st.sidebar.success("Select a UI tool.")
