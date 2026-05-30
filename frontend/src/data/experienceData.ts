export interface ExperienceDetail {
  title: string;
  period: string;
  location: string;
  role: string;
  description: string;
  achievements: { type: string; desc: string }[];
  techStack: string[];
}

export const experienceData: Record<
  string,
  {
    companyName: string;
    folderName: string;
    files: Record<string, ExperienceDetail>;
  }
> = {
  linfra_corp: {
    companyName: "LINFRA Corp.",
    folderName: "linfra_corp",
    files: {
      "ERP_Controller.md": {
        title: "LINFRA Corp.",
        period: "Aug 2023 - Present",
        location: "On-site - Philippines",
        role: "ERP Associate / Asset, IT & Data Management Controller",
        description:
          "Bridge end-users and developers to manage, administer, and enhance the C# ASP.NET-based ERP system, while handling hardware/software assets, QA/data audits, and cross-department IT support.",
        achievements: [
          {
            type: "MANAGED",
            desc: "Managed hardware repairs, device provisioning, and an employee asset allocation registry across the organization.",
          },
          {
            type: "ADMINISTERED",
            desc: "Administered and enhanced a C# ASP.NET-based ERP — triaging bugs, coordinating with developers, and improving modules across Asset Management, QA, HRIS, and Project Management.",
          },
          {
            type: "AUDITED",
            desc: "Conducted QA/data audits on engineering documentation and generated management reports from ERP data.",
          },
          {
            type: "CHAMPIONED",
            desc: "Led cross-department IT support and championed AI tool adoption to modernize operational workflows.",
          },
        ],
        techStack: [
          "DATA MANAGEMENT",
          "HARDWARE MANAGEMENT",
          "SOFTWARE MANAGEMENT",
          "SQL",
          "ERP",
          "QA TESTING",
          "AI_TOOLS",
        ],
      },
    },
  },
  richwell_phils: {
    companyName: "Richwell Phils. Inc.",
    folderName: "richwell_phils",
    files: {
      "Warehouse_Staff.md": {
        title: "Richwell Phils. Inc.",
        period: "Aug 2022 - July 2023",
        location: "On-site - Philippines",
        role: "Warehouse System Staff",
        description:
          "Provided system administration and first-level tech support while managing order routing and encoding operations.",
        achievements: [
          {
            type: "ROUTED",
            desc: "Handled order encoding, product allocation, and routing across warehouse locations and receivers.",
          },
          {
            type: "RESOLVED",
            desc: "Provided first-level tech support: network troubleshooting, server configuration, and basic hardware repair.",
          },
        ],
        techStack: ["NETWORKING", "SERVERS", "HARDWARE", "IT_SUPPORT"],
      },
    },
  },
  root_files: {
    companyName: "Root",
    folderName: "",
    files: {
      "README.sh": {
        title: "Career Summary Overview",
        period: "2022 - Present",
        location: "Philippines",
        role: "IT Specialist & Fullstack Developer",
        description:
          "IT professional with nearly 4 years of experience bridging end-users and developers — administering ERP systems, managing hardware/software assets, and building full-stack solutions. Passionate about integrating AI tools into real operational workflows and delivering data-driven insights.",
        achievements: [
          {
            type: "BRIDGING",
            desc: "Bridging end-users and developers to deliver robust system enhancements and clear data reporting.",
          },
          {
            type: "ADAPTING",
            desc: "Passionate about integrating AI tools into real operational workflows and delivering data-driven insights.",
          },
        ],
        techStack: [
          "JAVASCRIPT",
          "TYPESCRIPT",
          "VUE.JS",
          "REACT",
          "NODE.JS",
          "PYTHON",
          "FASTAPI",
          "SQL",
          "MONGODB",
          "ERP",
          "QA",
          "AI_TOOLS",
        ],
      },
    },
  },
};
