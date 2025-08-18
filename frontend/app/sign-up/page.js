import { useState } from "react";

export default function Signup() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    month: "",
    day: "",
    year: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-200">
      <div className="w-full max-w-lg rounded-2xl bg-white p-8 shadow-lg">
        {/* Close + Logo */}
        <div className="flex items-center justify-between">
          <button className="text-2xl">&times;</button>
          <span className="text-xl font-bold">X</span>
          <span></span>
        </div>

        <h1 className="mt-6 text-2xl font-bold">Create your account</h1>

        {/* Name */}
        <div className="mt-6">
          <label className="block text-sm font-medium">Name</label>
          <input
            type="text"
            name="name"
            value={form.name}
            onChange={handleChange}
            maxLength={50}
            className="mt-1 w-full rounded-lg border p-3 focus:border-blue-500 focus:ring focus:ring-blue-200"
          />
          <div className="mt-1 text-right text-xs text-gray-500">
            {form.name.length} / 50
          </div>
        </div>

        {/* Email */}
        <div className="mt-4">
          <label className="block text-sm font-medium">Email</label>
          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            className="mt-1 w-full rounded-lg border p-3 focus:border-blue-500 focus:ring focus:ring-blue-200"
          />
        </div>

        {/* DOB */}
        <div className="mt-6">
          <label className="block text-sm font-semibold">Date of birth</label>
          <p className="text-xs text-gray-500">
            This will not be shown publicly. Confirm your own age, even if this
            account is for a business, a pet, or something else.
          </p>
          <div className="mt-3 flex gap-2">
            <select
              name="month"
              value={form.month}
              onChange={handleChange}
              className="w-1/3 rounded-lg border p-3 focus:border-blue-500 focus:ring focus:ring-blue-200"
            >
              <option value="">Month</option>
              {[
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
              ].map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
            <select
              name="day"
              value={form.day}
              onChange={handleChange}
              className="w-1/3 rounded-lg border p-3 focus:border-blue-500 focus:ring focus:ring-blue-200"
            >
              <option value="">Day</option>
              {Array.from({ length: 31 }, (_, i) => i + 1).map((d) => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>
            <select
              name="year"
              value={form.year}
              onChange={handleChange}
              className="w-1/3 rounded-lg border p-3 focus:border-blue-500 focus:ring focus:ring-blue-200"
            >
              <option value="">Year</option>
              {Array.from({ length: 100 }, (_, i) => 2025 - i).map((y) => (
                <option key={y} value={y}>
                  {y}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Next Button */}
        <button
          disabled={!form.name || !form.email || !form.month || !form.day || !form.year}
          className={`mt-6 w-full rounded-full py-3 font-semibold transition ${
            form.name && form.email && form.month && form.day && form.year
              ? "bg-black text-white hover:opacity-90"
              : "bg-gray-300 text-gray-500"
          }`}
        >
          Next
        </button>
      </div>
    </div>
  );
}
