export default async function getPost(id) {
 // Call FastAPI backend
 const res = await fetch(`/api/posts/${id}`, {
  cache: "no-store", // Always fetch fresh data
 });

 if (!res.ok) {
  throw new Error("Failed to fetch post");
 }

 const data = await res.json();
 return data;
}