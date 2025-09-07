"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";

export default function Post() {
  const [content, setContent] = useState("");
  const [mediaUrl, setMediaUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handlePost = async () => {
    if (!content.trim() && !mediaUrl.trim()) {
      setError("Post must have at least content or media.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/posts", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          content,
          reply_to_post_id: null, 
          repost_of_post_id: null, 
          is_repost: false,
          media_url: mediaUrl || null,
          media_items: mediaUrl
            ? [{ file_url: mediaUrl, type: "image" }]
            : null, // adjust if you add more media types
        }),
      });

      const data = await response.json();
      setLoading(false);

      if (response.ok) {
        console.log("✅ Post created:", data);
        // redirect to timeline/home
        window.location.href = "/";
      } else {
        setError(data.detail || "Failed to post");
      }
    } catch (err) {
      console.error(err);
      setError("Something went wrong");
      setLoading(false);
    }
  };

  return (
    <div id="post-component">
      <nav>
        <Link href="/">
          <button id="return-button">
            <svg viewBox="0 0 24 24">
              <g>
                <path d="M7.414 13l5.043 5.04-1.414 1.42L3.586 12l7.457-7.46 1.414 1.42L7.414 11H21v2H7.414z"></path>
              </g>
            </svg>
          </button>
        </Link>
        <button id="post-button" onClick={handlePost} disabled={loading}>
          {loading ? "Posting..." : "Post"}
        </button>
      </nav>

      <div id="textarea-container">
        <Image
          className="textarea-profile-image"
          src={"/emma.jpeg"}
          height={40}
          width={40}
          alt="profile-image"
        />
        <textarea
          placeholder="What’s happening?"
          className="post-textarea"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        ></textarea>
      </div>

      <div id="media-container">
        <input
          type="text"
          placeholder="Media URL (optional)"
          value={mediaUrl}
          onChange={(e) => setMediaUrl(e.target.value)}
        />
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}
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