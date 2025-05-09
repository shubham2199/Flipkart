import pandas as pd
from langchain_core.documents import Document

def dataconvertor():
    product_data = pd.read_csv("data\\flipkart_laptop_data.csv")
    
    # Create a empty list for or whole product
    product_details = []

    # Iterate over the rows of the DataFrame

    for index, row in product_data.iterrows():
        object_list = {
            "Product_Name" : row["Product_Name"],
            "Prices" : row["Prices"],
            "Reviews" : row["Reviews"],
            "Processor" : row["Processor"],
            "RAM" : row["RAM"],
            "Operating System" : row["Operating System"],
            "SSD" : row["SSD"],
            "Display" : row["Display"],
            "Year Warranty" :row["Year Warranty"]
        }
        
    # Append the object list to the product details
    product_details.append(object_list)
        
        
    docs = []

    for object in product_details:
        metadata = {
            "Product_Name" : object["Product_Name"],
            "Prices" : object["Prices"],
            "Reviews" : object["Reviews"],
            "Processor" : object["Processor"],
            "RAM" : object["RAM"],
            "Operating System" : object["Operating System"],
            "SSD" : object["SSD"],
            "Display" : object["Display"]
        }
        page_content =object["Year Warranty"]
        doc_detail = Document(page_content= page_content, metadata= metadata)
        docs.append(doc_detail)
    return docs