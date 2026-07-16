function StudentProfile() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [semester, setSemester] = useState("");
  
  return (
    <section className="max-w-6xl mx-auto px-4 py-6">
      <h3 className="text-xl font-semibold mb-2">Student Profile</h3>
      <form className="grid gap-2 sm:grid-cols-3">
        <input
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="border p-2"
        />
        <input
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border p-2"
        />
        <input
          placeholder="Semester"
          value={semester}
          onChange={(e) => setSemester(e.target.value)}
          className="border p-2"
        />
      </form>
    </section>
  );
}