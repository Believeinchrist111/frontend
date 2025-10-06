"use client";

import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "next/navigation";
import Link from "next/link.js";


import PostNav from "../../../ui/post-nav.js"
import PostpageTweetCard from "../../../ui/postpage-tweet-card.js"
import ReplyCard from "@/app/ui/reply-card.js";
import FooterNav from "../../../ui/footer-nav.js"
import SideNav from "../../../ui/side-nav";
import "./postpage.css"



import { fetchUser } from "@/app/lib/slices/userSlice";
import { getPost, setReplyTarget } from "@/app/lib/slices/postSlice";


export default function PostPage() {
  const [togglePost, setTogglePost] = useState(false)

  const { id } = useParams(); // dynamic URL params
  const dispatch = useDispatch()
  const { user } = useSelector((state) => state.user);
  const { post, loading } = useSelector((state) => state.posts)


  useEffect(() => {
    dispatch(getPost(id))
  }, [id, dispatch]);

  console.log(post)
  if (loading) return <p>Loading...</p>;
  if (!post) return <p>Post not found</p>;

  return (
    <>
      <div id="postpage-body">

        <PostNav />

        <section id="postpage-section">
          <PostpageTweetCard postInfo={post} />

          {post.replies.map((replyInfo) => (
            <div key={replyInfo.id}>
              <ReplyCard replyInfo={replyInfo} />
            </div>
          ))}
        </section>

        <SideNav user={user} />
        <FooterNav />

        <Link href='/compose/post' onClick={() => dispatch(setReplyTarget(post))}>
          <button id="compose-button">
            <svg viewBox="0 0 24 24" className="post-icon">
              <g><path d="M1.751 10c0-4.42 3.584-8 8.005-8h4.366c4.49 0 8.129 3.64 8.129 8.13 0 2.96-1.607 5.68-4.196 7.11l-8.054 4.46v-3.69h-.067c-4.49.1-8.183-3.51-8.183-8.01zm8.005-6c-3.317 0-6.005 2.69-6.005 6 0 3.37 2.77 6.08 6.138 6.01l.351-.01h1.761v2.3l5.087-2.81c1.951-1.08 3.163-3.13 3.163-5.36 0-3.39-2.744-6.13-6.129-6.13H9.756z"></path></g>
            </svg>
          </button>
        </Link>
      </div>
    </>
  );
}
