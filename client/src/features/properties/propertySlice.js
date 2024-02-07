import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import propertyAPIService from "./propertyAPIService";

/* 
slice; application state is seperated 
into slices(small portions of state) by use of createSlice function
*/

const initialState = {
  isError: false,
  isLoading: false,
  isSuccess: false,
  message: "",
  properties: [],
};

// thunk to get all properties - this is the action creator
export const fetchProperties = createAsyncThunk(
  "properties/fetchAll",
  async (_, thunkAPI) => {
    try {
      return await propertyAPIService.fetchProperties();
    } catch (error) {
      const message =
        (error.response &&
          error.response.data &&
          error.response.data.message) ||
        error.message ||
        error.toString();

      return thunkAPI.rejectWithValue(message);
    }
  }
);

export const propertySlice = createSlice({
  name: "properties",
  initialState: initialState,
  reducers: {
    // standard reducer logic, with auto-generated action types per reducer
    reset: (state) => initialState,
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchProperties.pending, (state) => {
        state.isLoading = true;
      })

      .addCase(fetchProperties.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSuccess = true;
        state.properties = action.payload.results;
      })

      .addCase(fetchProperties.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
      })

      // and provide a default case if no other handlers matched
      .addDefaultCase((state, action) => {})
  },
});

export const { reset } = propertySlice.actions;
export default propertySlice.reducer;
