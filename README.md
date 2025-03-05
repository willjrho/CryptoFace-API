# CryptoFace-API

Example of a Langgraph agent wrapped into an API for wide front end distribution. 

This API has a single endpoint which is used to recieved tx data from a front end, send data to a crypto langgraph agent with 2 abilities - parse said data for a musd tx and parse said data for a btc tx. The api reponds with data that is ready to be used to build / submit a tx with a web3 wallet such as Taho. 
