import { type PayloadAction, createSlice } from "@reduxjs/toolkit";

const initialState = {};

export const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setAuthData: (_state, action: PayloadAction) => {
      return action.payload;
    },
  },
});

export const { setAuthData } = authSlice.actions;

export const authReducer = authSlice.reducer;

export default authSlice.reducer;
