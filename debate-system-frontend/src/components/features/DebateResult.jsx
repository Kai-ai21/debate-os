// src/components/features/DebateResult.jsx
// ─────────────────────────────────────────────────────────────────────────────
// A DUMB component that receives a complete debate result object and renders it.
// It makes no API calls. It manages no state. It simply transforms data into UI.
// This is the simplest possible component — a pure rendering function.
//
// EXPECTED SHAPE OF THE 'result' PROP (matches your FastAPI response):
// {
//   topic: "Should AI have legal rights?",
//   proponent_argument: "AI systems demonstrate...",
//   critic_argument: "However, current AI lacks...",
//   moderator_verdict: "After weighing both sides...",
//   confidence_score: 0.78,
//   risks: ["Premature legal personhood", "Accountability gaps"],
//   blind_spots: ["Long-term societal impact"],
//   timestamp: "2024-01-15T14:30:00Z"
// }
// ─────────────────────────────────────────────────────────────────────────────

// Helper component — a "sub-component" for a styled section card.
// We define it in the same file because it's only used here.
// When a sub-component grows complex or is used elsewhere, extract it.
import ReactMarkdown from "react-markdown";

const Section = ({ title, content, accentColor = "#646cff", icon }) => {
  if (!content) return null;

  const text =
    typeof content === "string"
      ? content
      : content?.argument ||
        content?.verdict ||
        content?.output ||
        JSON.stringify(content);

  return (
    <div
      style={{
        backgroundColor: "#1a1a2e",
        border: `1px solid ${accentColor}33`,
        borderLeft: `4px solid ${accentColor}`,
        borderRadius: "12px",
        padding: "2rem",
        marginBottom: "1.5rem",
      }}
    >
      <h3
        style={{
          color: accentColor,
          margin: "0 0 1rem 0",
          fontSize: "0.85rem",
          fontWeight: "700",
          textTransform: "uppercase",
          letterSpacing: "0.08em",
        }}
      >
        {icon} {title}
      </h3>

      <ReactMarkdown
        components={{
          p: ({ children }) => (
            <p
              style={{
                color: "#e5e7eb",
                lineHeight: "1.9",
                marginBottom: "1rem",
                whiteSpace: "pre-wrap",
              }}
            >
              {children}
            </p>
          ),

          li: ({ children }) => (
            <li
              style={{
                color: "#e5e7eb",
                lineHeight: "1.8",
                marginBottom: "0.5rem",
              }}
            >
              {children}
            </li>
          ),

          strong: ({ children }) => (
            <strong
              style={{
                color: "#ffffff",
                fontWeight: "700",
              }}
            >
              {children}
            </strong>
          ),
        }}
      >
        {text}
      </ReactMarkdown>
    </div>
  );
};

// Helper component for rendering lists (risks, blind spots)
const ListSection = ({ title, items, accentColor, icon }) => {

  if (!items || items.length === 0) return null;

  return (
    <div
      style={{
        backgroundColor: "#1a1a2e",
        border: `1px solid ${accentColor}33`,
        borderLeft: `4px solid ${accentColor}`,
        borderRadius: "12px",
        padding: "1.5rem",
        marginBottom: "1rem",
      }}
    >
      <h3
        style={{
          color: accentColor,
          margin: "0 0 0.75rem 0",
          fontSize: "0.85rem",
          fontWeight: "700",
          textTransform: "uppercase",
          letterSpacing: "0.08em",
        }}
      >
        {icon} {title}
      </h3>

      <ul
        style={{
          margin: 0,
          paddingLeft: "1.5rem",
          color: "#e5e7eb",
        }}
      >
        {items.map((item, i) => (
          <li
            key={i}
            style={{
              color: "#e5e7eb",
              lineHeight: "1.9",
              marginBottom: "0.75rem",
            }}
          >
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
};

const DebateResult = ({
  proponent,
  critic,
  moderator,
}) => {

  if (!proponent && !critic && !moderator) {
    return null;
  }

  return (
    <div>

      <Section
        title="Proponent Argument"
        content={proponent}
        accentColor="#22c55e"
        icon="🟢"
      />

      <Section
        title="Critic Argument"
        content={critic}
        accentColor="#ef4444"
        icon="🔴"
      />

      <Section
        title="Moderator Verdict"
        content={moderator?.verdict || moderator}
        accentColor="#646cff"
        icon="⚖️"
      />

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "1rem",
        }}
      >

        <ListSection
          title="Identified Risks"
          items={moderator?.risks}
          accentColor="#f97316"
          icon="⚠️"
        />

        <ListSection
          title="Blind Spots"
          items={moderator?.blind_spots}
          accentColor="#8b5cf6"
          icon="🔍"
        />

      </div>

    </div>
  );
};

export default DebateResult;