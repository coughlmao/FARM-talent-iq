import { ChevronRightIcon, Code2Icon } from "lucide-react";
import Navbar from "../components/Navbar.jsx";
import { Link } from "react-router";

import { PROBLEMS } from "../data/problems.js";
import { getDifficultyBadgeClass } from "../lib/utils.js";

const ProblemsPage = () => {
  const problems = Object.values(PROBLEMS);

  const easyProblemsCount = problems.filter(
    (p) => p.difficulty === "Easy"
  ).length;
  const mediumProblemsCount = problems.filter(
    (p) => p.difficulty === "Medium"
  ).length;
  const hardProblemsCount = problems.filter(
    (p) => p.difficulty === "Hard"
  ).length;

  return (
    <div className="min-h-screen bg-base-200">
      {/* Navbar */}
      <Navbar />

      <div className="max-w-6xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Practice Problems</h1>
          <p className="text-base-content/70">
            Sharpen your coding skills with these curated problems
          </p>
        </div>

        {/* Problems List */}
        <div className="space-y-4">
          {problems.map((problem) => (
            <Link
              key={problem.id}
              to={`/problems/${problem.id}`}
              className="card bg-base-100 hover:scale-[1.01] transition-transform"
            >
              <div className="card-body">
                <div className="flex items-center justify-between gap-4">
                  {/* Left Side */}
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-lg bg-primary/10 flex items-center justify-center ">
                        <Code2Icon className="w-5 h-5 sm:w-6 sm:h-6 text-primary" />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <h2 className="text-base sm:text-xl font-bold">
                            {problem.title}
                          </h2>
                          <span
                            className={`badge badge-sm text-xs sm:text-sm ${getDifficultyBadgeClass(
                              problem.difficulty
                            )}`}
                          >
                            {problem.difficulty}
                          </span>
                        </div>
                        <p className="text-sm text-base-content/60">
                          {problem.category}
                        </p>
                      </div>
                    </div>
                    <p className="text-sm sm:text-base text-base-content/80 mb-3">
                      {problem.description.text}
                    </p>
                  </div>

                  {/* Right Side */}
                  <div className="flex items-center gap-2 text-primary">
                    <span className="font-md text-sm sm:text-base">Solve</span>
                    <ChevronRightIcon className="w-4 h-4 sm:w-5 sm:h-5" />
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>

        {/* Stats Footer */}
        <div className="mt-12 card bg-base-100 shadow-lg">
          <div className="card-body">
            <div className="stats stats-horizontal">
              <div className="stat">
                <div className="stat-title">Total Problems</div>
                <div className="stat-value text-primary text-2xl sm:text-4xl">
                  {problems.length}
                </div>
              </div>

              <div className="stat">
                <div className="stat-title">Easy</div>
                <div className="stat-value text-success text-2xl sm:text-4xl">
                  {easyProblemsCount}
                </div>
              </div>

              <div className="stat">
                <div className="stat-title">Medium</div>
                <div className="stat-value text-warning text-2xl sm:text-4xl">
                  {mediumProblemsCount}
                </div>
              </div>

              <div className="stat">
                <div className="stat-title">Hard</div>
                <div className="stat-value text-error text-2xl sm:text-4xl">
                  {hardProblemsCount}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProblemsPage;
