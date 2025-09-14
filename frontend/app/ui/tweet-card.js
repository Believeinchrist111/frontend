import "./tweet-card.css"




export default function TweetCard({ user, post }) {
  const mediaCount = post.media_items?.length || 0;

  return (
    <div id="tweet-card">
      <div id="profile-info">
        <div id="profile-image"></div>
        <div id="handle-container">
          <div id="user-name">
            {user.firstname} {user.lastname}
          </div>
          <div id="user-account-name">@IAmMarkManson</div>
        </div>
        <button type="button">...</button>
      </div>

      <div id="tweet-content-interact-wrapper">
        {post.content && <p id="tweet-message">{post.content}</p>}

        {/* Media section */}
        {mediaCount > 0 && (
          <div
            id="tweet-media"
            className={
              mediaCount === 2
                ? "two"
                : mediaCount === 3
                  ? "three"
                  : mediaCount === 4
                    ? "four"
                    : ""
            }
          >

            {post.media_items?.map((media, index) => (
              <div className="media-wrapper" key={index}>
                {media.type === "image" ? (
                  <img src={media.file_url} alt={`media-${index}`} />
                ) : (
                  <video controls>
                    <source src={media.file_url} type="video/mp4" />
                    Your browser does not support the video tag.
                  </video>
                )}
              </div>
            ))}

          </div>
        )}

        {/* ... The comment/repost/like/bookmark/share buttons ... */}
        <div id="tweet-interactions">
          <div className="comment">
            <svg viewBox="0 0 24 24" className="comment-icon"><g><path d="M1.751 10c0-4.42 3.584-8 8.005-8h4.366c4.49 0 8.129 3.64 8.129 8.13 0 2.96-1.607 5.68-4.196 7.11l-8.054 4.46v-3.69h-.067c-4.49.1-8.183-3.51-8.183-8.01zm8.005-6c-3.317 0-6.005 2.69-6.005 6 0 3.37 2.77 6.08 6.138 6.01l.351-.01h1.761v2.3l5.087-2.81c1.951-1.08 3.163-3.13 3.163-5.36 0-3.39-2.744-6.13-6.129-6.13H9.756z"></path></g></svg>
          </div>
          <div className="repost">
            <svg viewBox="0 0 24 24" className="repost-icon"><g><path d="M4.5 3.88l4.432 4.14-1.364 1.46L5.5 7.55V16c0 1.1.896 2 2 2H13v2H7.5c-2.209 0-4-1.79-4-4V7.55L1.432 9.48.068 8.02 4.5 3.88zM16.5 6H11V4h5.5c2.209 0 4 1.79 4 4v8.45l2.068-1.93 1.364 1.46-4.432 4.14-4.432-4.14 1.364-1.46 2.068 1.93V8c0-1.1-.896-2-2-2z"></path></g></svg>
          </div>
          <div className="like">
            <svg viewBox="0 0 24 24" className="like-icon"><g><path d="M16.697 5.5c-1.222-.06-2.679.51-3.89 2.16l-.805 1.09-.806-1.09C9.984 6.01 8.526 5.44 7.304 5.5c-1.243.07-2.349.78-2.91 1.91-.552 1.12-.633 2.78.479 4.82 1.074 1.97 3.257 4.27 7.129 6.61 3.87-2.34 6.052-4.64 7.126-6.61 1.111-2.04 1.03-3.7.477-4.82-.561-1.13-1.666-1.84-2.908-1.91zm4.187 7.69c-1.351 2.48-4.001 5.12-8.379 7.67l-.503.3-.504-.3c-4.379-2.55-7.029-5.19-8.382-7.67-1.36-2.5-1.41-4.86-.514-6.67.887-1.79 2.647-2.91 4.601-3.01 1.651-.09 3.368.56 4.798 2.01 1.429-1.45 3.146-2.1 4.796-2.01 1.954.1 3.714 1.22 4.601 3.01.896 1.81.846 4.17-.514 6.67z"></path></g></svg>
          </div>
          <div className="bookmark">
            <svg viewBox="0 0 24 24" className="bookmark-icon"><g><path d="M4 4.5C4 3.12 5.119 2 6.5 2h11C18.881 2 20 3.12 20 4.5v18.44l-8-5.71-8 5.71V4.5zM6.5 4c-.276 0-.5.22-.5.5v14.56l6-4.29 6 4.29V4.5c0-.28-.224-.5-.5-.5h-11z"></path></g></svg>
          </div>
          <div className="share">
            <svg viewBox="0 0 24 24" className="share-icon"><g><path d="M17 4c-1.1 0-2 .9-2 2 0 .33.08.65.22.92C15.56 7.56 16.23 8 17 8c1.1 0 2-.9 2-2s-.9-2-2-2zm-4 2c0-2.21 1.79-4 4-4s4 1.79 4 4-1.79 4-4 4c-1.17 0-2.22-.5-2.95-1.3l-4.16 2.37c.07.3.11.61.11.93s-.04.63-.11.93l4.16 2.37c.73-.8 1.78-1.3 2.95-1.3 2.21 0 4 1.79 4 4s-1.79 4-4 4-4-1.79-4-4c0-.32.04-.63.11-.93L8.95 14.7C8.22 15.5 7.17 16 6 16c-2.21 0-4-1.79-4-4s1.79-4 4-4c1.17 0 2.22.5 2.95 1.3l4.16-2.37c-.07-.3-.11-.61-.11-.93zm-7 4c-1.1 0-2 .9-2 2s.9 2 2 2c.77 0 1.44-.44 1.78-1.08.14-.27.22-.59.22-.92s-.08-.65-.22-.92C7.44 10.44 6.77 10 6 10zm11 6c-.77 0-1.44.44-1.78 1.08-.14.27-.22.59-.22.92 0 1.1.9 2 2 2s2-.9 2-2-.9-2-2-2z"></path></g>
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}




// export default function TweetCard({ user, post }) {
//   return (
//     <div id="tweet-card">

//       <div id="profile-info">
//         <div id="profile-image"></div>
//         <div id="handle-container">
//           <div id="user-name">{user.firstname} {user.lastname}</div>
//           <div id="user-account-name">@IAmMarkManson</div>
//         </div>
//         <button type="button">...</button>
//       </div>

//       <p id="tweet-message">{post.content}</p>
//       <div
//         id="tweet-media"
//         className={
//           post.media?.length === 2
//             ? "two"
//             : post.media?.length === 3
//               ? "three"
//               : post.media?.length === 4
//                 ? "four"
//                 : ""
//         }
//       >
//         {post.media?.map((file, idx) => (
//           <img key={idx} src={file.url} alt="tweet media" />
//         ))}
//       </div>

//       {/* <p id="tweet-message">Burn out doesn’t come from having too much to do—it comes from not doing the things that actually matter to you.
//      <br />
//      The weight you carry isn’t the work itself, but the meaninglessness of it.</p> */}

//       <div id="tweet-interactions">
//         <div className="comment">
//           <svg viewBox="0 0 24 24" className="comment-icon"><g><path d="M1.751 10c0-4.42 3.584-8 8.005-8h4.366c4.49 0 8.129 3.64 8.129 8.13 0 2.96-1.607 5.68-4.196 7.11l-8.054 4.46v-3.69h-.067c-4.49.1-8.183-3.51-8.183-8.01zm8.005-6c-3.317 0-6.005 2.69-6.005 6 0 3.37 2.77 6.08 6.138 6.01l.351-.01h1.761v2.3l5.087-2.81c1.951-1.08 3.163-3.13 3.163-5.36 0-3.39-2.744-6.13-6.129-6.13H9.756z"></path></g></svg>
//         </div>
//         <div className="repost">
//           <svg viewBox="0 0 24 24" className="repost-icon"><g><path d="M4.5 3.88l4.432 4.14-1.364 1.46L5.5 7.55V16c0 1.1.896 2 2 2H13v2H7.5c-2.209 0-4-1.79-4-4V7.55L1.432 9.48.068 8.02 4.5 3.88zM16.5 6H11V4h5.5c2.209 0 4 1.79 4 4v8.45l2.068-1.93 1.364 1.46-4.432 4.14-4.432-4.14 1.364-1.46 2.068 1.93V8c0-1.1-.896-2-2-2z"></path></g></svg>
//         </div>
//         <div className="like">
//           <svg viewBox="0 0 24 24" className="like-icon"><g><path d="M16.697 5.5c-1.222-.06-2.679.51-3.89 2.16l-.805 1.09-.806-1.09C9.984 6.01 8.526 5.44 7.304 5.5c-1.243.07-2.349.78-2.91 1.91-.552 1.12-.633 2.78.479 4.82 1.074 1.97 3.257 4.27 7.129 6.61 3.87-2.34 6.052-4.64 7.126-6.61 1.111-2.04 1.03-3.7.477-4.82-.561-1.13-1.666-1.84-2.908-1.91zm4.187 7.69c-1.351 2.48-4.001 5.12-8.379 7.67l-.503.3-.504-.3c-4.379-2.55-7.029-5.19-8.382-7.67-1.36-2.5-1.41-4.86-.514-6.67.887-1.79 2.647-2.91 4.601-3.01 1.651-.09 3.368.56 4.798 2.01 1.429-1.45 3.146-2.1 4.796-2.01 1.954.1 3.714 1.22 4.601 3.01.896 1.81.846 4.17-.514 6.67z"></path></g></svg>
//         </div>
//         <div className="bookmark">
//           <svg viewBox="0 0 24 24" className="bookmark-icon"><g><path d="M4 4.5C4 3.12 5.119 2 6.5 2h11C18.881 2 20 3.12 20 4.5v18.44l-8-5.71-8 5.71V4.5zM6.5 4c-.276 0-.5.22-.5.5v14.56l6-4.29 6 4.29V4.5c0-.28-.224-.5-.5-.5h-11z"></path></g></svg>
//         </div>
//         <div className="share">
//           <svg viewBox="0 0 24 24" className="share-icon"><g><path d="M17 4c-1.1 0-2 .9-2 2 0 .33.08.65.22.92C15.56 7.56 16.23 8 17 8c1.1 0 2-.9 2-2s-.9-2-2-2zm-4 2c0-2.21 1.79-4 4-4s4 1.79 4 4-1.79 4-4 4c-1.17 0-2.22-.5-2.95-1.3l-4.16 2.37c.07.3.11.61.11.93s-.04.63-.11.93l4.16 2.37c.73-.8 1.78-1.3 2.95-1.3 2.21 0 4 1.79 4 4s-1.79 4-4 4-4-1.79-4-4c0-.32.04-.63.11-.93L8.95 14.7C8.22 15.5 7.17 16 6 16c-2.21 0-4-1.79-4-4s1.79-4 4-4c1.17 0 2.22.5 2.95 1.3l4.16-2.37c-.07-.3-.11-.61-.11-.93zm-7 4c-1.1 0-2 .9-2 2s.9 2 2 2c.77 0 1.44-.44 1.78-1.08.14-.27.22-.59.22-.92s-.08-.65-.22-.92C7.44 10.44 6.77 10 6 10zm11 6c-.77 0-1.44.44-1.78 1.08-.14.27-.22.59-.22.92 0 1.1.9 2 2 2s2-.9 2-2-.9-2-2-2z"></path></g>
//           </svg>
//         </div>
//       </div>
//     </div>
//   );
// }

{/*   
                {post.media_items.map((item, idx) =>
                  item.type === "image" ? (
                    <div id="tweet-img-vid" key={idx}>
                      <img
                        src={item.file_url.replace(/\\/g, "/")} // fix Windows-style slashes
                        alt="tweet media"
                      />
                    </div>
                  ) : (
                    <div id="tweet-img-vid" key={idx}>
                      <video
                        controls
                        muted
                        loop
                        src={item.file_url.replace(/\\/g, "/")}
                      />
                    </div>
                  )
                )} */}