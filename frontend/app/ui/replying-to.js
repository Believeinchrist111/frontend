import "./replying-to.css"


export default function ReplyingTo({ replyTargetInfo }) {
 const mediaCount = replyTargetInfo.media_items?.length || 0;

 return (
  <div id="replying-to-card">

   <div id="profile-info">
    <div id="profile-image"></div>
    <div id="handle-container">
     <div id="user-name">
      {replyTargetInfo.owner.firstname} {replyTargetInfo.owner.lastname}
     </div>
     <div id="user-account-name">@IAmMarkManson</div>
    </div>
   </div>


   <div id="replying-to-content-wrapper">
    {replyTargetInfo.content && <p id="replying-to-message">{replyTargetInfo.content}</p>}

    {/* Media section */}
    {mediaCount > 0 && (
     <div
      id="postpage-tweet-media"
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

      {replyTargetInfo.media_items?.map((media, index) => (
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

    <p id="replying-to-text">Replying to <span>@{replyTargetInfo.owner.firstname} {replyTargetInfo.owner.lastname}</span></p>

   <div id="line"></div>
   </div>
  </div>
 );
}

