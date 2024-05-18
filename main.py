import requests
import streamlit as st

def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from the API.")
        return None

def identify_citations(response_data):
    citations = []
    if 'data' in response_data:
        response_objects = response_data['data']['data']
        for obj in response_objects:
            response_text = obj.get('response', '')
            sources = obj.get('source', [])
            for source in sources:
                if source['id'] and source['link']:
                    citations.append({"id": source['id'], "link": source['link']})
                    break
                elif source['link']:
                    citations.append({"id": "", "link": source['link']})
                    break
            else:
                citations.append({"id": "", "link": ""})
    else:
        st.warning("Response doesn't contain 'data' key.")
    return citations

def main():
    st.title("Citations Viewer")
    api_url = "https://devapi.beyondchats.com/api/get_message_with_sources"
    response_data = fetch_data(api_url)
    if response_data:
        citations = identify_citations(response_data)
        st.subheader("Citations:")
        if citations:
            for citation in citations:
                st.write(f"ID: {citation['id']}, Link: {citation['link']}")
        else:
            st.write("No citations found.")

if __name__ == "__main__":
    main()
