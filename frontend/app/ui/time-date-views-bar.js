
import "./time-date-views-bar.css"


function formatTweetDate(postCreationInfo) {
 const date = new Date(postCreationInfo);

 // Format time (e.g. "6:54 PM")
 const time = date.toLocaleTimeString("en-US", {
  hour: "numeric",
  minute: "2-digit",
  hour12: true,
 });

 // Format date (e.g. "Sep 21, 2025")
 const formattedDate = date.toLocaleDateString("en-US", {
  month: "short",
  day: "numeric",
  year: "numeric",
 });

 // Fake views count formatter (convert 1500000 -> "1.5M")
 function formatViews(views) {
  if (views >= 1_000_000) return (views / 1_000_000).toFixed(1) + "M";
  if (views >= 1_000) return (views / 1_000).toFixed(1) + "K";
  return views.toString();
 }

 const views = formatViews(1500000); // Example: replace with actual views

 // return `${time} · ${formattedDate} · ${views} Views`;
 return { time, formattedDate, views }
}




export default function TimeDateViewsBar({ postCreationInfo }) {
 console.log(postCreationInfo)

 // Example usage
 const info = formatTweetDate(postCreationInfo);


 return (
  <>
   <div id="time-date-views-bar">
    <span className="time">
     {info.time} · {info.formattedDate} · <span className="views">{info.views}</span> Views</span>
   </div>
  </>


 );
}

