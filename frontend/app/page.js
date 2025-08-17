import { cookies } from "next/headers";

import Home from "./home/page.js"
import "./page.css";

export default async function HomeWrapper() {
  const cookieStore = await cookies();
  const token = cookieStore.get("token")?.value || null;


  return (
    <>
        <Home token={token} />
    </>

  );
}

