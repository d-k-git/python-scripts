# Python scripts to work with Google Ads API 

To get access to the Google Ads reports via API you need to create a yaml file with four arguments:  developer_token,  client_id, client_secret  and refresh_token (also you can add here the client_customer_id, but I prefer add it in the main python file)

![image](https://user-images.githubusercontent.com/79371232/110238729-44039d00-7f54-11eb-8747-2ae3c1c92d92.png)

googleads.yaml content:

![image](https://user-images.githubusercontent.com/79371232/110238895-19661400-7f55-11eb-97e5-000985f7e52f.png)

A DEVELOPER_TOKEN  you get in your Google Ads account settings: 
![image](https://user-images.githubusercontent.com/79371232/110239087-33542680-7f56-11eb-90f4-613008848870.png)

Here how to get CLIENT_ID and CLIENT_SECRET:
https://developers.google.com/adwords/api/docs/guides/authentication#create_a_client_id_and_client_secret

A REFRESH_TOKEN  is generated in the terminal with the command: 

$ python generate_refresh_token.py --client_id INSERT_CLIENT_ID --client_secret INSERT_CLIENT_SECRET

File generate_refresh_token.py is downloaded from here:  https://github.com/googleads/googleads-python-lib/tree/master/examples/adwords/authentication




