import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import authService from "./authService";

const user = JSON.parse(localStorage.getItem("token"));
console.log("user from local storage === ", user);

const initialState = {
  user: user ? user : null,
  isSuccess: false,
  isError: false,
  isLoading: false,
  message: "",
};

const handleError = (error, thunkAPI) => {
  const message =
    (error.response && error.response.data && error.response.data.message) ||
    error.message ||
    error.toString();
  return thunkAPI.rejectWithValue(message);
};

export const register = createAsyncThunk(
  "auth/userRegister",
  async (data, thunkAPI) => {
    try {
      return await authService.register(data);
    } catch (error) {
      handleError(error, thunkAPI);
    }
  }
);

export const activateUser = createAsyncThunk(
  "auth/activate",
  async (data, thunkAPI) => {
    try {
      return await authService.activateUser(data);
    } catch (error) {
      handleError(error, thunkAPI);
    }
  }
);

export const login = createAsyncThunk(
  "auth/userLogin",
  async (credentials, thunkAPI) => {
    try {
      return await authService.login(credentials);
    } catch (error) {
      handleError(error, thunkAPI);
    }
  }
);

export const logout = createAsyncThunk("auth/signout", () => authService.logout());

export const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    reset: (state) => {
      // return state synchronously
      state.isLoading = false;
      state.isError = false;
      state.isSuccess = false;
      state.message = "";
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(register.pending, (state) => {
        state.isLoading = true;
      })

      .addCase(register.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSuccess = true;
        state.user = action.payload;
      })

      .addCase(register.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.user = null;
        state.message = action.payload;
      })

      .addCase(login.pending, (state) => {
        state.isLoading = true;
      })

      .addCase(login.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSuccess = true;
        state.user = action.payload;
      })

      .addCase(login.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
        state.user = null;
      })

      .addCase(activateUser.pending, (state) => {
        state.isLoading = true;
      })

      .addCase(activateUser.fulfilled, (state) => {
        state.isLoading = false;
        state.isSuccess = true;
      })

      .addCase(activateUser.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
        state.user = null;
      })

      .addCase(logout.fulfilled, (state) => {
        state.user = null;
      })

      .addDefaultCase((state, action) => {});
  },
});

export const { reset } = authSlice.actions;
export default authSlice.reducer;
