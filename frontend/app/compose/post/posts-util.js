// This function gets the token from the cookies 
import { cookies } from 'next/headers';

function getToken() {
  const requestCookies = cookies();
  return requestCookies.get("token")?.value;
}

export const token = getToken()