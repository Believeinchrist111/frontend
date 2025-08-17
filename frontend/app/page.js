import { cookies } from "next/headers";

import Home from "./home/page.js"
// import SignUpOrIn from "./sign-up-in/page.js"
import "./page.css";

export default async function HomeWrapper() {
  const cookieStore = await cookies();
  const token = cookieStore.get("token")?.value || null;

  console.log("server component")
  console.log(token)

  return (
    <>
        <Home token={token} />
    </>

  );
}

