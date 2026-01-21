import { useUser } from "@clerk/clerk-react";
import { ArrowRightIcon, SparklesIcon, ZapIcon } from "lucide-react";

const WelcomeSection = ({ onCreateSession }) => {
  const { user } = useUser();

  return (
    <div className="relative">
      <div className="relative max-w-7xl mx-auto px-6 py-16">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 rounded-2xl bg-linear-to-br from-primary to-secondary flex items-center justify-center">
                <SparklesIcon className="w-6 h-6 text-white" />
              </div>
              <h1 className="text-2xl sm:text-3xl md:text-4xl font-black bg-linear-to-r from-primary via-secondary to-accent bg-clip-text text-transparent leading-tight">
                Welcome back, {user?.firstName || "there"}!
              </h1>
            </div>
            <p className="text-lg sm:text-xl md:text-2xl text-base-content/60 sm:ml-16 ml-0 leading-tight">
              Ready to level up your coding skills?
            </p>
          </div>

          <button
            onClick={onCreateSession}
            className="group self-start sm:self-auto inline-flex items-center gap-3 w-auto px-4 py-2 sm:px-8 sm:py-4 bg-linear-to-r from-primary to-secondary rounded-2xl transition-all duration-200 hover:opacity-90 overflow-visible"
          >
            <ZapIcon className="w-5 h-5 sm:w-6 md:w-7 text-white shrink-0" />
            <span className="whitespace-nowrap font-bold text-sm sm:text-lg text-white">
              Create Session
            </span>
            <span className="ml-2 shrink-0 transform group-hover:translate-x-1 transition-transform">
              <ArrowRightIcon className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
            </span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default WelcomeSection;
