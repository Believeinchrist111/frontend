"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { Smile, Image as ImageIcon } from "lucide-react";

import "./page.css"

export default function Post() {
 const [content, setContent] = useState("");
 const [media, setMedia] = useState([]);
 const [loading, setLoading] = useState(false);
 const [error, setError] = useState("");



 // Handle multiple uploads
 const handleMediaChange = (e) => {
  const files = Array.from(e.target.files);
  const newMedia = files.map((file) => ({
   file,
   preview: URL.createObjectURL(file),
  }));
  setMedia((prev) => [...prev, ...newMedia]);
 };

 // Remove single file
 const removeMedia = (index) => {
  setMedia((prev) => prev.filter((_, i) => i !== index));
 };

 const handlePost = async () => {
  if (!content.trim() && media.length === 0) {
   setError("Post must have at least content or media.");
   return;
  }

  setLoading(true);
  setError("");

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

    if (!uploadRes.ok) throw new Error("Failed to upload media");

    const uploadData = await uploadRes.json();
    uploadedMediaItems = uploadData.media_items; // [{ file_url, type }]
   }

   // Step 2: Create the post with uploaded media
   const response = await fetch("/api/posts", {
    method: "POST",
    headers: {
     "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({
     content,
     reply_to_post_id: null,
     repost_of_post_id: null,
     is_repost: false,
     media_items: uploadedMediaItems.length > 0 ? uploadedMediaItems : null,
    }),
   });

   if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to create post");
   }

   const data = await response.json();
   console.log("Post created:", data);

   setContent("");
   setMedia([]);
  } catch (err) {
   setError(err.message || "Something went wrong");
  } finally {
   setLoading(false);
  }
 };

 return (
  <div id="post-component">
   <div id="post-wrapper">
    <nav>
     <Link href="/">
      <button id="return-button">
       <svg viewBox="0 0 24 24"><g><path d="M7.414 13l5.043 5.04-1.414 1.42L3.586 12l7.457-7.46 1.414 1.42L7.414 11H21v2H7.414z"></path></g>
       </svg>
      </button>
     </Link>

     <button id="post-button" onClick={handlePost} disabled={loading}>
      {loading ? "Posting..." : "Post"}
     </button>
    </nav>

    <div id="textarea-container">
     <div id="textarea-img-container">
      <Image
       className="profile-img"
       src={"/emma.jpeg"}
       height={40}
       width={40}
       alt="profile-image"
      />

      <textarea
       placeholder="What’s happening?"
       value={content}
       onChange={(e) => setContent(e.target.value)}
       className="post-textarea"
       rows={3}
      />

     </div>

     {/* Media preview */}
     {media.length > 0 && (
      <div className="media-grid">
       {media.map((m, index) => (
        <div key={index} className="media-item">
         {m.file.type.startsWith("image/") ? (
          <img src={m.preview} alt="preview" />
         ) : (
          <video src={m.preview} controls />
         )}
         <button
          className="remove-media"
          onClick={() => removeMedia(index)}
         >
          {/* <X size={18} /> */}
         </button>
        </div>
       ))}
      </div>
     )}


     <div id="toolbar">
      <div className="tools-left">
       <label className="icon-btn">
        <input
         type="file"
         accept="image/*,video/*"
         hidden
         multiple
         onChange={handleMediaChange}
        />
        <ImageIcon size={20} />
       </label>
       <button type="button" className="icon-btn">
        <Smile size={20} />
       </button>
      </div>

      <button
       className={`post-btn ${content.trim() || media.length ? "active" : ""}`}
       disabled={!content.trim() && !media.length}
      >
       Post
      </button>
     </div>

     {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
   </div>
  </div>
 );
}

















// import Image from "next/image";
// import Link from "next/link";
// import "./page.css"


// export default function Post() {

//  return (
//   <div id="post-component">
//    <nav>
//     <Link href="/">
//      <button id="return-button">
//       <svg viewBox="0 0 24 24" className=""><g><path d="M7.414 13l5.043 5.04-1.414 1.42L3.586 12l7.457-7.46 1.414 1.42L7.414 11H21v2H7.414z"></path></g></svg>
//      </button>
//     </Link>
//     <button id="post-button">Post</button>
//    </nav>
//    <div id="textarea-container">
//     <Image
//      className="textarea-profile-image"
//      src={'/emma.jpeg'}
//      height={40}
//      width={40}
//      alt="profile-image"
//     />
//     <textarea placeholder="What’s happening?" className="post-textarea" ></textarea>
//    </div>
//   </div>

//  );
// }