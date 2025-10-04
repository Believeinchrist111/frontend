import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

// Thunk: Fetch posts from backend
export const fetchReplies = createAsyncThunk("posts/fetchReplies", async (postId) => {
  const res = await fetch(`/api/posts/${postId}`, { 
   credentials: "include" 
  });

  if (!res.ok) throw new Error("Failed to fetch replies");
  
  return await res.json();
});

// Thunk for creating a new post
export const createReplies = createAsyncThunk(
  "posts/createReplies",
  async ({ postId, content, media }, { rejectWithValue }) => {
    try {
      // Step 1: Upload files if any
      let uploadedMediaItems = [];
      if (media.length > 0) {
        const formData = new FormData();
        media.forEach((m) => formData.append("files", m.file));

        const uploadRes = await fetch("http://127.0.0.1:8000/upload-media", {
          method: "POST",
          body: formData,
        });

        if (!uploadRes.ok) {
          throw new Error("Failed to upload media");
        }

        const uploadData = await uploadRes.json();
        uploadedMediaItems = uploadData.media_items; // [{ file_url, type }]
      }

      // Step 2: Create the post with uploaded media
      const response = await fetch(`/api/posts/${postId}/create_reply`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", 
        body: JSON.stringify({
          content,
          reply_to_post_id: postId,
          repost_of_post_id: null,
          is_repost: false,
          media_items: uploadedMediaItems.length > 0 ? uploadedMediaItems : null,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to create reply");
      }

      const data = await response.json();
      return data; // resolved value available in fulfilled reducer
    } catch (err) {
      return rejectWithValue(err.message || "Something went wrong");
    }
  }
);

const replySlice = createSlice({
  name: "replies",
  initialState: {
    replies: [],       // all replies to a post
    loading: false, // whether fetching or creating is happening
    error: null,    // error messages
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      // Fetch replies
      .addCase(fetchReplies.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchReplies.fulfilled, (state, action) => {
        state.loading = false;
        state.replies = action.payload;
      })
      .addCase(fetchReplies.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })

      // Create reply
      .addCase(createReplies.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createReplies.fulfilled, (state, action) => {
        state.loading = false;
        state.replies.unshift(action.payload); // add new post to top
      })
      .addCase(createReplies.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default replySlice.reducer;
