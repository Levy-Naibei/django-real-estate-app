import axios from "axios"

const config = {
    headers: {
        "Content-Type": "application/json"
    }
}

// signs up new users
const register = async(data) => {
    const response = await axios.post("/api/v1/auth/users/", data, config);
    console.log("register res == ", response.data);
    return response.data
}

// activates registered user account
const activateUser = async(data) => {
    const response = await axios.post("/api/v1/auth/users/activation/", data, config);
    console.log("activation res == ", response.data);
    return response.data;
}

// logs in user
const login = async(credentials) => {
    const response = await axios.post("/ap1/v1/auth/jwt/create/", credentials, config);
    
    if (response.data) {
        console.log("token == ", JSON.stringify(response.data))
        localStorage.setItem("token", JSON.stringify(response.data));
    } else {
        if (response.data.email !== credentials.email || response.data.password !== credentials.password) {
            throw Error("Error! check your credentials")
        }
    }

    console.log("login res == ", response.data);
    return response.data;
}

// logs out user
const logout = () => localStorage.removeItem("token");

const authService = { login, register, activateUser, logout };
export default authService;
