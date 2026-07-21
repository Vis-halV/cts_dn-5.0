// TASK 1: CREATE THE COLLECTION AND INSERT DOCUMENTS

use py_fse

db.createCollection("feedback")

db.feedback.insertMany([
  {
    student_id:   9,
    course_code:  "CS101",
    semester:     "2022-ODD",
    rating:       5,
    comments:     "Excellent teaching. Concepts were very clear.",
    tags:         ["challenging", "well-structured", "good-examples"],
    submitted_at: ISODate("2022-11-30T10:15:00Z"),
    attachments:  [{ filename: "notes.pdf", size_kb: 240 }]
  },
  {
    student_id:   11,
    course_code:  "CS101",
    semester:     "2022-ODD",
    rating:       4,
    comments:     "Good course but assignments were tough.",
    tags:         ["challenging", "assignments-heavy"],
    submitted_at: ISODate("2022-11-28T09:00:00Z"),
    attachments:  [{ filename: "hw1.pdf", size_kb: 120 }]
  },
  {
    student_id:   14,
    course_code:  "CS101",
    semester:     "2021-ODD",
    rating:       2,
    comments:     "Too fast-paced. Needed more examples.",
    tags:         ["fast-paced", "needs-improvement"],
    submitted_at: ISODate("2021-11-20T14:30:00Z"),
    attachments:  []
  },
  {
    student_id:   10,
    course_code:  "CS102",
    semester:     "2022-ODD",
    rating:       5,
    comments:     "Best database course I have taken.",
    tags:         ["well-structured", "practical", "good-examples"],
    submitted_at: ISODate("2022-11-25T11:00:00Z"),
    attachments:  [{ filename: "db_notes.pdf", size_kb: 380 }]
  },
  {
    student_id:   13,
    course_code:  "CS102",
    semester:     "2022-EVEN",
    rating:       3,
    comments:     "Average experience. Content was okay.",
    tags:         ["average", "needs-improvement"],
    submitted_at: ISODate("2022-05-10T08:45:00Z"),
    attachments:  [{ filename: "summary.docx", size_kb: 90 }]
  },
  {
    student_id:   12,
    course_code:  "CS103",
    semester:     "2022-ODD",
    rating:       4,
    comments:     "OOP concepts explained very well.",
    tags:         ["well-structured", "practical"],
    submitted_at: ISODate("2022-11-22T16:00:00Z"),
    attachments:  [{ filename: "oop_summary.pdf", size_kb: 200 }]
  },
  {
    student_id:   16,
    course_code:  "EC101",
    semester:     "2021-EVEN",
    rating:       1,
    comments:     "Very difficult. Lecturer was not approachable.",
    tags:         ["difficult", "needs-improvement", "fast-paced"],
    submitted_at: ISODate("2021-05-15T13:20:00Z"),
    attachments:  [{ filename: "circuit_notes.pdf", size_kb: 310 }]
  },
  {
    student_id:   17,
    course_code:  "ME101",
    semester:     "2022-ODD",
    rating:       3,
    comments:     "Decent course. Could use more lab sessions.",
    tags:         ["average", "practical"],
    submitted_at: ISODate("2022-11-18T10:30:00Z"),
    attachments:  [{ filename: "thermo_notes.pdf", size_kb: 150 }]
  },
  {
    student_id:   18,
    course_code:  "CS101",
    semester:     "2021-EVEN",
    rating:       2,
    comments:     "Confusing at times. Needs better structure.",
    tags:         ["challenging", "needs-improvement"],
    submitted_at: ISODate("2021-05-20T09:15:00Z"),
    attachments:  [{ filename: "cs101_notes.pdf", size_kb: 175 }]
  },
  {
    student_id:   19,
    course_code:  "CS102",
    semester:     "2022-ODD",
    rating:       5,
    comments:     "Loved every lecture. Highly recommended.",
    tags:         ["well-structured", "good-examples", "practical"],
    submitted_at: ISODate("2022-11-29T12:00:00Z")
  }

])

db.feedback.countDocuments()

db.feedback.find().pretty()

// TASK 2: CRUD OPERATIONS

// STEP 5: READ — All feedback where rating = 5
db.feedback.find(
  { rating: 5 }
).pretty()


// STEP 6: READ — CS101 feedback where tags contains
//          'challenging'
db.feedback.find(
  {
    course_code: "CS101",
    tags:        "challenging"
  }
).pretty()

// STEP 7: READ — Projection: return only student_id,
//          course_code, and rating — exclude _id
db.feedback.find(
  {},
  { student_id: 1, course_code: 1, rating: 1, _id: 0 }
)

// STEP 8: UPDATE — Add needs_review: true to all documents

// Update
db.feedback.updateMany(
  { rating: { $lt: 3 } },
  { $set: { needs_review: true } }
)

// Verify
db.feedback.find(
  { needs_review: true },
  { student_id: 1, course_code: 1, rating: 1, needs_review: 1, _id: 0 }
)

// STEP 9: UPDATE — Push the tag 'reviewed' into the tags
//          array of all documents where needs_review = true
db.feedback.updateMany(
  { needs_review: true },
  { $push: { tags: "reviewed" } }
)

// Verify 
db.feedback.find(
  { needs_review: true },
  { student_id: 1, course_code: 1, tags: 1, _id: 0 }
)

// STEP 70: DELETE — Remove all feedback for semester 2021-EVEN

// Delete
db.feedback.deleteMany({ semester: "2021-EVEN" })

// Verify
db.feedback.countDocuments()

// TASK 3: AGGREGATION PIPELINE
db.feedback.aggregate([
  {
    $match: { semester: "2022-ODD" }
  },
  {
    $group: {
      _id:            "$course_code",
      avg_rating:     { $avg: "$rating" },
      feedback_count: { $sum: 1 }
    }
  },
  {
    $sort: { avg_rating: -1 }
  }

])

db.feedback.countDocuments()                   
db.feedback.find().sort({ course_code: 1 }).pretty()
db.feedback.getIndexes()                       