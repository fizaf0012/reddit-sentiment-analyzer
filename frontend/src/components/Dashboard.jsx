// src/components/Dashboard.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  LineChart,
  Line,
  CartesianGrid,
  Legend,
} from "recharts";

const COLORS = { positive: "#22c55e", negative: "#ef4444", neutral: "#9ca3af" };

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [subreddit, setSubreddit] = useState("");
  const [posts, setPosts] = useState([]);
  const [sentimentSummary, setSentimentSummary] = useState({
    positive: 0,
    negative: 0,
    neutral: 0,
    emotions: {},
  });
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("Overview");

  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  // Auth check
  useEffect(() => {
    if (!token) {
      navigate("/login");
      return;
    }
    axios
      .get("http://localhost:8000/users/me", { headers: { Authorization: `Bearer ${token}` } })
      .then((res) => {
        setUser(res.data);
        localStorage.setItem("role", res.data.role);
      })
      .catch(() => {
        localStorage.removeItem("token");
        localStorage.removeItem("role");
        navigate("/login");
      });
  }, [navigate, token]);

  // Fetch & analyze subreddit
  const handleFetch = async () => {
    const trimmedSubreddit = subreddit.trim();
    if (!trimmedSubreddit) return alert("Enter subreddit name.");
    setLoading(true);

    try {
      const res = await axios.get(
        `http://localhost:8000/reddit/fetch/${trimmedSubreddit}?limit=10`,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      const fetchedPosts = res.data.results || [];
      const summary = fetchedPosts.reduce(
        (acc, post) => {
          const s = post.sentiment?.toLowerCase();
          if (s && acc[s] !== undefined) acc[s]++;
          const e = post.emotion?.toLowerCase();
          if (e && e !== "neutral") acc.emotions[e] = (acc.emotions[e] || 0) + 1;
          return acc;
        },
        { positive: 0, negative: 0, neutral: 0, emotions: {} }
      );

      setPosts(fetchedPosts);
      setSentimentSummary(summary);
      fetchHistory(trimmedSubreddit);
    } catch (err) {
      console.error("Error fetching subreddit:", err);
      alert("Error fetching subreddit data.");
    } finally {
      setLoading(false);
    }
  };

  const fetchHistory = async (name) => {
    try {
      const res = await axios.get(`http://localhost:8000/reddit/history/${name}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const hist = Array.isArray(res.data) ? res.data : res.data.results || [];
      setHistory(hist.slice(0, 10));
    } catch (err) {
      console.error("Error fetching history:", err);
    }
  };

  if (!user) return <div className="p-6">Loading dashboard...</div>;

  const pieData = [
    { name: "Positive", value: sentimentSummary.positive },
    { name: "Negative", value: sentimentSummary.negative },
    { name: "Neutral", value: sentimentSummary.neutral },
  ];
  const barData = Object.entries(sentimentSummary.emotions).map(([name, value]) => ({ name, value }));
  const lineData = posts.map((p, i) => ({ index: i + 1, confidence: p.confidence }));

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar activeTab={activeTab} onSelect={setActiveTab} />

      <div className="flex flex-col flex-1">
        <Topbar />

        <main className="p-6 overflow-y-auto">
          {activeTab === "Overview" && (
            <>
              {/* Greeting */}
              <div className="mb-6 bg-white p-4 rounded-xl shadow flex justify-between items-center">
                <div>
                  <h2 className="text-lg font-semibold text-gray-700">Welcome, {user.username} 👋</h2>
                  <p className="text-sm text-gray-500">Role: {user.role}</p>
                </div>
                {user.role === "admin" && (
                  <button
                    onClick={() => navigate("/admin")}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg shadow hover:bg-blue-700"
                  >
                    Go to Admin Panel
                  </button>
                )}
              </div>

              {/* Subreddit search */}
              <div className="bg-white p-6 rounded-xl shadow mb-6">
                <h2 className="text-xl font-semibold mb-4">Subreddit Sentiment Analyzer</h2>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={subreddit}
                    onChange={(e) => setSubreddit(e.target.value)}
                    placeholder="Enter subreddit name..."
                    className="flex-1 border p-2 rounded-lg"
                  />
                  <button
                    onClick={handleFetch}
                    className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
                  >
                    {loading ? "Analyzing..." : "Fetch & Analyze"}
                  </button>
                </div>
              </div>

              {/* Summary cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div className="bg-white p-6 rounded-xl shadow text-center">
                  <h2 className="font-semibold text-gray-700">Positive</h2>
                  <p className="text-3xl font-bold text-green-600">{sentimentSummary.positive}</p>
                </div>
                <div className="bg-white p-6 rounded-xl shadow text-center">
                  <h2 className="font-semibold text-gray-700">Negative</h2>
                  <p className="text-3xl font-bold text-red-600">{sentimentSummary.negative}</p>
                </div>
                <div className="bg-white p-6 rounded-xl shadow text-center">
                  <h2 className="font-semibold text-gray-700">Neutral</h2>
                  <p className="text-3xl font-bold text-gray-500">{sentimentSummary.neutral}</p>
                </div>
              </div>

              {/* Charts */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                <div className="bg-white p-4 rounded-xl shadow">
                  <h3 className="font-semibold mb-2">Sentiment Distribution</h3>
                  <PieChart width={300} height={250}>
                    <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                      {pieData.map((entry, i) => (
                        <Cell key={`cell-${i}`} fill={Object.values(COLORS)[i]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </div>

                <div className="bg-white p-4 rounded-xl shadow">
                  <h3 className="font-semibold mb-2">Emotion Frequency</h3>
                  <BarChart width={300} height={250} data={barData}>
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#3b82f6" />
                  </BarChart>
                </div>

                <div className="bg-white p-4 rounded-xl shadow">
                  <h3 className="font-semibold mb-2">Confidence Trend</h3>
                  <LineChart width={300} height={250} data={lineData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="index" />
                    <YAxis domain={[0, 1]} />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="confidence" stroke="#f59e0b" strokeWidth={2} />
                  </LineChart>
                </div>
              </div>

              {/* Table */}
              <div className="bg-white p-6 rounded-xl shadow mb-6">
                <h3 className="text-lg font-semibold mb-4">Analysis Results</h3>
                <table className="min-w-full border">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="p-2 border">Title</th>
                      <th className="p-2 border">Sentiment</th>
                      <th className="p-2 border">Emotion</th>
                      <th className="p-2 border">Confidence</th>
                      <th className="p-2 border">Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    {posts.map((p) => (
                      <tr key={p.id} className="text-sm">
                        <td className="p-2 border text-blue-600">
                          <a href={p.url} target="_blank" rel="noreferrer">
                            {p.title}
                          </a>
                        </td>
                        <td
                          className={`p-2 border font-semibold ${
                            p.sentiment === "positive"
                              ? "text-green-600"
                              : p.sentiment === "negative"
                              ? "text-red-600"
                              : "text-gray-600"
                          }`}
                        >
                          {p.sentiment}
                        </td>
                        <td className="p-2 border capitalize">{p.emotion}</td>
                        <td className="p-2 border">{p.confidence?.toFixed(2)}</td>
                        <td className="p-2 border">{p.score}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* History */}
              <div className="bg-white p-6 rounded-xl shadow">
                <h3 className="text-lg font-semibold mb-4">Recent Analyses</h3>
                <ul className="list-disc ml-6 text-gray-700">
                  {history.map((h, idx) => (
                    <li key={idx}>
                      {h.subreddit || subreddit} — {h.average_sentiment || h.sentiment}
                    </li>
                  ))}
                </ul>
              </div>
            </>
          )}

          {activeTab === "Trends" && (
            <div className="bg-white p-6 rounded-xl shadow">
              <h2 className="text-xl font-semibold mb-4">Subreddit Trends</h2>
              <p>Here you can add visualizations specifically for trends.</p>
            </div>
          )}

          {activeTab === "Settings" && (
            <div className="bg-white p-6 rounded-xl shadow">
              <h2 className="text-xl font-semibold mb-4">Settings</h2>
              <p>User preferences and settings can go here.</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
