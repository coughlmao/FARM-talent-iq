import { TrophyIcon, UsersIcon } from "lucide-react";

const StatsCards = ({ activeSessionsCount, recentSessionsCount }) => {
  return (
    <div className="lg:col-span-1 grid grid-cols-1 gap-6">
      {/* Active Count */}
      <div className="card bg-base-100 border-2 border-primary/20 hover:border-primary/40 min-h-28 sm:min-h-32 relative">
        <div className="absolute top-3 right-3">
          <div className="badge badge-primary text-xs sm:text-sm">Live</div>
        </div>

        <div className="card-body p-3 sm:p-4 flex flex-col items-start justify-center">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-3 bg-primary/10 rounded-2xl flex items-center justify-center">
              <UsersIcon className="w-6 h-6 text-primary" />
            </div>
          </div>

          <div className="text-4xl sm:text-5xl font-black leading-tight text-left">
            {activeSessionsCount}
          </div>
          <div className="text-sm opacity-60 mt-1 text-left">
            Active Sessions
          </div>
        </div>
      </div>

      {/* Total / Recent Count */}
      <div className="card bg-base-100 border-2 border-secondary/20 hover:border-secondary/40 min-h-28 sm:min-h-32 relative">
        <div className="card-body p-3 sm:p-4 flex flex-col items-start justify-center">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-3 bg-secondary/10 rounded-2xl flex items-center justify-center">
              <TrophyIcon className="w-6 h-6 text-secondary" />
            </div>
          </div>

          <div className="text-4xl sm:text-5xl font-black leading-tight text-left">
            {recentSessionsCount}
          </div>
          <div className="text-sm opacity-60 mt-1 text-left">
            Total Sessions
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatsCards;
