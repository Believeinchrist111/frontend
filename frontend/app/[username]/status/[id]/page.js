"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link.js";

import getPost from "../../../lib/api/postFetch.js"

import PostNav from "../../../ui/post-nav.js"
import PostpageTweetCard from "../../../ui/postpage-tweet-card.js"
import ReplyCard from "@/app/ui/reply-card.js";
import FooterNav from "../../../ui/footer-nav.js"
import SideNav from "../../../ui/side-nav";



export default function PostPage() {
  const { id } = useParams(); // dynamic URL params
  const [postInfo, setPostInfo] = useState(null);
  const [replies, setReplies] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadPost = async () => {
      try {
        const data = await getPost(id);
        setPostInfo(data);
      } catch (err) {
        console.error("Failed to fetch post:", err);
      } finally {
        setLoading(false);
      }
    }

    if (id) loadPost();
  }, [id]);


  if (loading) return <p>Loading...</p>;
  if (!postInfo) return <p>Post not found</p>;

  return (
    <>
      <div id="postpage-body">
        <PostNav />
        <section id="postpage-section">
          <PostpageTweetCard postInfo={postInfo} />
          <ReplyCard replyInfo={replies} />
        </section>

        {/* <SideNav user={user} /> */}
        <FooterNav />

        <Link href='/compose/post'>
          <button id="compose-button" onClick={() => setTogglePost(!togglePost)}>
            <svg viewBox="0 0 24 24" className="reply-icon"><g><path d="M1.751 10c0-4.42 3.584-8 8.005-8h4.366c4.49 0 8.129 3.64 8.129 8.13 0 2.96-1.607 5.68-4.196 7.11l-8.054 4.46v-3.69h-.067c-4.49.1-8.183-3.51-8.183-8.01zm8.005-6c-3.317 0-6.005 2.69-6.005 6 0 3.37 2.77 6.08 6.138 6.01l.351-.01h1.761v2.3l5.087-2.81c1.951-1.08 3.163-3.13 3.163-5.36 0-3.39-2.744-6.13-6.129-6.13H9.756z"></path></g></svg>
          </button>
        </Link>
      </div>
    </>
  );
}
