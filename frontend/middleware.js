import { NextResponse } from "next/server";

export async function middleware(request) {
 const token = request.cookies.get("token")?.value;

 if (!token) {
  return NextResponse.redirect(new URL("/sign-up-in", request.url));
 }

 const verify = await fetch("http://127.0.0.1:8000/verify-token", {
  method: "GET",
  headers: {
   Authorization: `Bearer ${token}`,
  },
 });

 if (!verify.ok) {
  return NextResponse.redirect(new URL("/sign-in", request.url));
 }

 return NextResponse.next();
}


export const config = {
 matcher: ["/", "/home"], // protect homepage
};

