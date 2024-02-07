import axios from "axios"

// get all properties
export const fetchProperties = async() => {
    const response = await axios.get("api/v1/properties/all/");
    console.log("properties === ", response.data)
    return response.data;
}

const propertyAPIService = { fetchProperties }
export default propertyAPIService;
