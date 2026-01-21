import {
  ArrowRightIcon,
  Code2Icon,
  CrownIcon,
  SparklesIcon,
  UsersIcon,
  ZapIcon,
  LoaderIcon,
} from "lucide-react";
import { Link } from "react-router";

import { getDifficultyBadgeClass } from "../lib/utils.js";

const ActiveSessions = ({ sessions, isLoading, isUserInSession }) => {
  return (
    <div className="lg:col-span-2 card bg-base-100 border-2 border-primary/20 hover:border-primary/30 h-full">
      <div className="card-body p-3 sm:p-6">
        {/* HEADERS SECTION */}
        <div className="flex items-center justify-between mb-4 sm:mb-6">
          <div className="flex items-center gap-2 sm:gap-3">
            <div className="p-2 bg-linear-to-r from-primary to-secondary rounded-xl">
              <ZapIcon className="w-4 h-4 sm:w-5 sm:h-5" />
            </div>
            <h2 className="text-xl sm:text-2xl font-black">Live Sessions</h2>
          </div>

          <div className="flex items-center gap-2">
            <div className="hidden sm:block w-2 h-2 bg-success rounded-full" />
            <span className="text-xs sm:text-sm font-medium text-success">
              {sessions.length} active
            </span>
          </div>
        </div>

        {/* SESSIONS LIST */}
        <div className="space-y-3 max-h-48 sm:max-h-100 overflow-y-auto pr-2">
          {isLoading ? (
            <div className="col-span-full flex items-center justify-center py-12 sm:py-20">
              <LoaderIcon className="w-8 h-8 sm:w-10 sm:h-10 animate-spin text-primary" />
            </div>
          ) : sessions.length > 0 ? (
            sessions.map((session) => (
              <div
                key={session._id}
                className="card bg-base-200 border-2 border-base-300 hover:border-primary/50"
              >
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-4 p-3 sm:p-5">
                  {/* LEFT SIDE */}
                  <div className="flex items-start sm:items-center gap-3 sm:gap-4 flex-1 min-w-0">
                    <div className="relative w-10 h-10 sm:w-14 sm:h-14 rounded-xl bg-linear-to-r from-primary to-secondary flex items-center justify-center shrink-0">
                      <Code2Icon className="w-4 h-4 sm:w-7 sm:h-7 text-white" />
                      <div className="absolute -top-1 -right-1 w-3 h-3 sm:w-4 sm:h-4 bg-success rounded-full border-2 border-base-100" />
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between sm:justify-start gap-2 mb-1">
                        <h3 className="font-bold text-sm sm:text-lg truncate">
                          {session.problem}
                        </h3>

                        {/* desktop inline difficulty with proper color */}
                        <span
                          className={`hidden sm:inline-block badge badge-sm ml-2 ${getDifficultyBadgeClass(
                            session.difficulty
                          )}`}
                        >
                          {session.difficulty?.slice(0, 1).toUpperCase() +
                            session.difficulty?.slice(1)}
                        </span>
                      </div>

                      <div className="flex items-center gap-3 text-xs sm:text-sm opacity-80">
                        <div className="flex items-center gap-1 min-w-0">
                          <CrownIcon className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
                          <span className="font-medium truncate">
                            {session.host?.name}
                          </span>
                        </div>
                        <div className="flex items-center gap-1">
                          <UsersIcon className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
                          <span className="text-xs">
                            {session.participant ? "2/2" : "1/2"}
                          </span>
                        </div>
                        {session.participant && !isUserInSession(session) ? (
                          <span className="badge badge-error badge-sm">
                            FULL
                          </span>
                        ) : (
                          <span className="badge badge-success badge-sm">
                            OPEN
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* MOBILE: inline badge + button with more gap and fixed max width to avoid stretching */}
                  <div className="sm:hidden inline-flex items-center gap-4 mt-2 self-start">
                    <span
                      className={`badge badge-sm ${getDifficultyBadgeClass(
                        session.difficulty
                      )}`}
                    >
                      {session.difficulty?.slice(0, 1).toUpperCase() +
                        session.difficulty?.slice(1)}
                    </span>

                    <div className="shrink-0">
                      {session.participant && !isUserInSession(session) ? (
                        <button className="btn btn-disabled btn-xs px-3 py-1 h-7 w-auto shrink-0">
                          Full
                        </button>
                      ) : (
                        <Link
                          to={`/session/${session._id}`}
                          className="btn btn-primary btn-xs px-3 py-1 gap-2 h-7 w-auto max-w-24 shrink-0"
                        >
                          {isUserInSession(session) ? "Rejoin" : "Join"}
                          <ArrowRightIcon className="w-4 h-4" />
                        </Link>
                      )}
                    </div>
                  </div>

                  {/* DESKTOP: action on the right */}
                  <div className="mt-2 sm:mt-0 shrink-0 hidden sm:flex">
                    {session.participant && !isUserInSession(session) ? (
                      <button className="btn btn-disabled btn-sm px-3 py-1 sm:px-4 sm:py-2">
                        Full
                      </button>
                    ) : (
                      <Link
                        to={`/session/${session._id}`}
                        className="btn btn-primary btn-sm gap-2 px-3 py-1 sm:px-4 sm:py-2 text-sm sm:text-base"
                      >
                        {isUserInSession(session) ? "Rejoin" : "Join"}
                        <ArrowRightIcon className="w-4 h-4" />
                      </Link>
                    )}
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-12 sm:py-16">
              <div className="w-16 h-16 mx-auto mb-4 bg-linear-to-r from-primary/20 to-secondary/20 rounded-3xl flex items-center justify-center">
                <SparklesIcon className="w-8 h-8 text-primary/50" />
              </div>
              <p className="text-base sm:text-lg font-semibold opacity-70 mb-1">
                No active sessions
              </p>
              <p className="text-sm opacity-50">Be the first to create one!</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ActiveSessions;
