#!/usr/bin/env bash
# ==============================================================================
# GraviDex Capabilities Suite - Universal Shell Installer
# Works with: Google Antigravity IDE, Claude Code, and OpenCode workspaces.
# ==============================================================================

set -e

# ANSI Color codes
if [ -t 1 ]; then
  BOLD="\033[1m"
  GREEN="\033[0;32m"
  CYAN="\033[0;36m"
  YELLOW="\033[1;33m"
  RED="\033[0;31m"
  DIM="\033[2m"
  RESET="\033[0m"
else
  BOLD=""
  GREEN=""
  CYAN=""
  YELLOW=""
  RED=""
  DIM=""
  RESET=""
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# All 21 Capabilities in Suite
ALL_SKILLS=(
  "autonomous-agent-engineering"
  "backend-engineering"
  "design-systems"
  "frontend-engineering"
  "interface-design"
  "quality-engineering"
  "security-audit"
  "technical-documentation"
  "agentshield"
  "asd-ste100"
  "awwwards"
  "boardui"
  "jury"
  "karpathy-guidelines"
  "last30days"
  "lemo-opuscar"
  "motionsites-web-builder"
  "rev-engineer"
  "scrapling"
  "skillforge"
  "stageshow"
)

# Bundles
BUNDLE_CURATED=(
  "autonomous-agent-engineering"
  "backend-engineering"
  "design-systems"
  "frontend-engineering"
  "interface-design"
  "quality-engineering"
  "security-audit"
  "technical-documentation"
)

BUNDLE_SPECIALISTS=(
  "agentshield"
  "asd-ste100"
  "awwwards"
  "boardui"
  "jury"
  "karpathy-guidelines"
  "last30days"
  "lemo-opuscar"
  "motionsites-web-builder"
  "rev-engineer"
  "scrapling"
  "skillforge"
  "stageshow"
)

BUNDLE_DESIGN=(
  "design-systems"
  "interface-design"
  "frontend-engineering"
  "awwwards"
  "boardui"
  "jury"
  "motionsites-web-builder"
  "lemo-opuscar"
  "stageshow"
)

BUNDLE_ENGINEERING=(
  "autonomous-agent-engineering"
  "backend-engineering"
  "quality-engineering"
  "security-audit"
  "technical-documentation"
  "agentshield"
  "asd-ste100"
  "karpathy-guidelines"
  "rev-engineer"
  "scrapling"
  "skillforge"
)

# State variables
MODE=""
CUSTOM_PATH=""
SELECTED_SKILLS=()
RUN_TESTS=false
DRY_RUN=false
INSTALL_ALL_FLAG=false
BUNDLE_NAME=""

resolve_skill_dir() {
  local skill="$1"
  if [ -d "$SCRIPT_DIR/CAPABILITIES/curated/$skill" ]; then
    echo "$SCRIPT_DIR/CAPABILITIES/curated/$skill"
  elif [ -d "$SCRIPT_DIR/CAPABILITIES/retained-specialists/$skill" ]; then
    echo "$SCRIPT_DIR/CAPABILITIES/retained-specialists/$skill"
  elif [ -d "$SCRIPT_DIR/.agents/skills/$skill" ]; then
    echo "$SCRIPT_DIR/.agents/skills/$skill"
  elif [ -d "$SCRIPT_DIR/skills/$skill" ]; then
    echo "$SCRIPT_DIR/skills/$skill"
  elif [ -d "$SCRIPT_DIR/$skill" ]; then
    echo "$SCRIPT_DIR/$skill"
  else
    echo ""
  fi
}

show_help() {
  cat << EOF
${BOLD}GraviDex Capabilities Suite - Universal Installer${RESET}

${BOLD}USAGE:${RESET}
    ./install.sh [OPTIONS]

${BOLD}DESTINATION OPTIONS:${RESET}
    -g, --global              Install globally for Antigravity IDE (~/.gemini/config/skills) [Default]
    -p, --project [DIR]       Install locally into project repository (.agents/skills)
    -c, --claude              Install globally for Claude Code (~/.claude/skills)
    --claude-project [DIR]    Install locally for Claude Code project (.claude/skills)
    --opencode                Install globally for OpenCode (~/.config/opencode/skills)
    --opencode-project [DIR]  Install locally for OpenCode project (.opencode/skills)
    --custom DIR              Install into custom target directory

${BOLD}SKILL SELECTION OPTIONS:${RESET}
    -a, --all                 Install all 21 capabilities without prompting
    -b, --bundle NAME         Install bundle: 'curated' (8), 'specialists' (13), 'design' (9), 'engineering' (11)
    -s, --skills LIST         Comma-separated list of skills to install
    -l, --list                List available capabilities and bundles
    -t, --test                Run test suite after installation
    -d, --dry-run             Simulate installation without copying files
    -h, --help                Show this help message

${BOLD}EXAMPLES:${RESET}
    ./install.sh --all --global          # Install all 21 capabilities globally
    ./install.sh --bundle curated -g     # Install 8 curated capability packs globally
    ./install.sh --bundle design -p      # Install design bundle into local project workspace
    ./install.sh                         # Launch guided interactive installer
EOF
  exit 0
}

list_skills() {
  echo -e "${BOLD}Available Capabilities in Suite (${#ALL_SKILLS[@]} total):${RESET}"
  echo -e "------------------------------------------------------------------------"
  for i in "${!ALL_SKILLS[@]}"; do
    printf "  %2d.  ${CYAN}%-32s${RESET}\n" "$((i + 1))" "${ALL_SKILLS[$i]}"
  done
  echo -e "\n${BOLD}Curated Bundles:${RESET}"
  echo -e "  - ${GREEN}curated${RESET}     (8 packs):  ${BUNDLE_CURATED[*]}"
  echo -e "  - ${GREEN}specialists${RESET} (11 skills): ${BUNDLE_SPECIALISTS[*]}"
  echo -e "  - ${GREEN}design${RESET}      (8 skills):  ${BUNDLE_DESIGN[*]}"
  echo -e "  - ${GREEN}engineering${RESET} (10 skills): ${BUNDLE_ENGINEERING[*]}"
  echo -e "------------------------------------------------------------------------"
  exit 0
}

# Parse CLI arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -g|--global)
      MODE="global"
      shift
      ;;
    -p|--project)
      MODE="project"
      if [[ -n "$2" && "$2" != -* ]]; then
        CUSTOM_PATH="$2"
        shift
      fi
      shift
      ;;
    -c|--claude)
      MODE="claude"
      shift
      ;;
    --claude-project)
      MODE="claude-project"
      if [[ -n "$2" && "$2" != -* ]]; then
        CUSTOM_PATH="$2"
        shift
      fi
      shift
      ;;
    --opencode)
      MODE="opencode"
      shift
      ;;
    --opencode-project)
      MODE="opencode-project"
      if [[ -n "$2" && "$2" != -* ]]; then
        CUSTOM_PATH="$2"
        shift
      fi
      shift
      ;;
    --custom)
      MODE="custom"
      CUSTOM_PATH="$2"
      shift 2
      ;;
    -a|--all)
      INSTALL_ALL_FLAG=true
      shift
      ;;
    -b|--bundle)
      BUNDLE_NAME="$2"
      shift 2
      ;;
    -s|--skills)
      IFS=',' read -r -a CLI_SKILLS <<< "$2"
      SELECTED_SKILLS=("${CLI_SKILLS[@]}")
      shift 2
      ;;
    -l|--list)
      list_skills
      ;;
    -t|--test)
      RUN_TESTS=true
      shift
      ;;
    -d|--dry-run)
      DRY_RUN=true
      shift
      ;;
    -h|--help)
      show_help
      ;;
    *)
      echo -e "${RED}Unknown option: $1${RESET}"
      show_help
      ;;
  esac
done

# Resolve bundles if specified via flag
if [ -n "$BUNDLE_NAME" ]; then
  case "$BUNDLE_NAME" in
    curated)
      SELECTED_SKILLS=("${BUNDLE_CURATED[@]}")
      ;;
    specialists)
      SELECTED_SKILLS=("${BUNDLE_SPECIALISTS[@]}")
      ;;
    design)
      SELECTED_SKILLS=("${BUNDLE_DESIGN[@]}")
      ;;
    engineering)
      SELECTED_SKILLS=("${BUNDLE_ENGINEERING[@]}")
      ;;
    *)
      echo -e "${RED}Error: Unknown bundle '$BUNDLE_NAME'. Choose from: curated, specialists, design, engineering${RESET}"
      exit 1
      ;;
  esac
elif [ "$INSTALL_ALL_FLAG" = true ]; then
  SELECTED_SKILLS=("${ALL_SKILLS[@]}")
fi

# Interactive mode if target mode or skills selection is missing
if [ -z "$MODE" ] || [ ${#SELECTED_SKILLS[@]} -eq 0 ]; then
  if [ -t 0 ]; then
    echo -e "${BOLD}${CYAN}========================================================================${RESET}"
    echo -e "${BOLD}       GraviDex Capabilities Suite - Guided Interactive Setup           ${RESET}"
    echo -e "${BOLD}${CYAN}========================================================================${RESET}\n"

    # Step 1: Destination
    if [ -z "$MODE" ]; then
      echo -e "${BOLD}Step 1: Choose destination:${RESET}\n"
      echo -e "  ${BOLD}1)${RESET} Antigravity Global        ${DIM}(~/.gemini/config/skills) [Recommended - Universal]${RESET}"
      echo -e "  ${BOLD}2)${RESET} Current Project Workspace ${DIM}(./.agents/skills)        [Project-scoped]${RESET}"
      echo -e "  ${BOLD}3)${RESET} Claude Code Global        ${DIM}(~/.claude/skills)        [Claude CLI]${RESET}"
      echo -e "  ${BOLD}4)${RESET} Claude Code Project       ${DIM}(./.claude/skills)${RESET}"
      echo -e "  ${BOLD}5)${RESET} OpenCode Global           ${DIM}(~/.config/opencode/skills)${RESET}"
      echo -e "  ${BOLD}6)${RESET} OpenCode Project          ${DIM}(./.opencode/skills)${RESET}"
      echo -e "  ${BOLD}7)${RESET} Custom Directory\n"
      read -rp "Select destination [1-7] (default: 1): " choice_dest
      choice_dest="${choice_dest:-1}"
      case "$choice_dest" in
        1) MODE="global" ;;
        2) MODE="project" ;;
        3) MODE="claude" ;;
        4) MODE="claude-project" ;;
        5) MODE="opencode" ;;
        6) MODE="opencode-project" ;;
        7)
          MODE="custom"
          read -rp "Enter target directory path: " CUSTOM_PATH
          ;;
        *)
          echo -e "${YELLOW}Defaulting to Antigravity Global.${RESET}"
          MODE="global"
          ;;
      esac
    fi

    # Step 2: Skill Scope
    if [ ${#SELECTED_SKILLS[@]} -eq 0 ]; then
      echo -e "\n${BOLD}Step 2: Choose capabilities to install:${RESET}\n"
      echo -e "  ${BOLD}1)${RESET} ${GREEN}Install All 21 Capabilities${RESET}    ${DIM}[Recommended - Complete Suite]${RESET}"
      echo -e "  ${BOLD}2)${RESET} Curated Capability Packs     ${DIM}(8 packs: autonomous-agent, backend, design...)${RESET}"
      echo -e "  ${BOLD}3)${RESET} Retained Specialists         ${DIM}(${#BUNDLE_SPECIALISTS[@]} skills: agentshield, asd-ste100, boardui...)${RESET}"
      echo -e "  ${BOLD}4)${RESET} Design & Frontend Bundle     ${DIM}(${#BUNDLE_DESIGN[@]} skills: design-systems, interface-design...)${RESET}"
      echo -e "  ${BOLD}5)${RESET} Engineering Bundle           ${DIM}(${#BUNDLE_ENGINEERING[@]} skills: autonomous-agent, backend, quality...)${RESET}"
      echo -e "  ${BOLD}6)${RESET} Custom Pick                  ${DIM}(Select by comma-separated numbers, e.g. 1, 8, 15)${RESET}\n"
      read -rp "Select skills [1-6] (default: 1): " choice_scope
      choice_scope="${choice_scope:-1}"
      case "$choice_scope" in
        1)
          SELECTED_SKILLS=("${ALL_SKILLS[@]}")
          ;;
        2)
          SELECTED_SKILLS=("${BUNDLE_CURATED[@]}")
          ;;
        3)
          SELECTED_SKILLS=("${BUNDLE_SPECIALISTS[@]}")
          ;;
        4)
          SELECTED_SKILLS=("${BUNDLE_DESIGN[@]}")
          ;;
        5)
          SELECTED_SKILLS=("${BUNDLE_ENGINEERING[@]}")
          ;;
        6)
          echo -e "\nAvailable capabilities:"
          for i in "${!ALL_SKILLS[@]}"; do
            printf "  %2d) %s\n" "$((i + 1))" "${ALL_SKILLS[$i]}"
          done
          read -rp $'\nEnter numbers or names separated by commas: ' raw_picks
          SELECTED_SKILLS=()
          IFS=',' read -r -a tokens <<< "$raw_picks"
          for tok in "${tokens[@]}"; do
            tok=$(echo "$tok" | xargs)
            if [[ "$tok" =~ ^[0-9]+$ ]]; then
              idx=$((tok - 1))
              if [ $idx -ge 0 ] && [ $idx -lt ${#ALL_SKILLS[@]} ]; then
                SELECTED_SKILLS+=("${ALL_SKILLS[$idx]}")
              fi
            elif [ -n "$tok" ]; then
              for s in "${ALL_SKILLS[@]}"; do
                if [ "$s" = "$tok" ]; then
                  SELECTED_SKILLS+=("$tok")
                  break
                fi
              done
            fi
          done
          if [ ${#SELECTED_SKILLS[@]} -eq 0 ]; then
            echo -e "${YELLOW}No valid skills selected. Defaulting to all ${#ALL_SKILLS[@]} capabilities.${RESET}"
            SELECTED_SKILLS=("${ALL_SKILLS[@]}")
          fi
          ;;
        *)
          SELECTED_SKILLS=("${ALL_SKILLS[@]}")
          ;;
      esac
    fi
  else
    # Non-interactive shell defaults
    [ -z "$MODE" ] && MODE="global"
    [ ${#SELECTED_SKILLS[@]} -eq 0 ] && SELECTED_SKILLS=("${ALL_SKILLS[@]}")
  fi
fi

# Resolve destination directory
TARGET_DIR=""
case "$MODE" in
  global)
    TARGET_DIR="$HOME/.gemini/config/skills"
    ;;
  project)
    BASE_DIR="${CUSTOM_PATH:-.}"
    TARGET_DIR="$BASE_DIR/.agents/skills"
    ;;
  claude)
    TARGET_DIR="$HOME/.claude/skills"
    ;;
  claude-project)
    BASE_DIR="${CUSTOM_PATH:-.}"
    TARGET_DIR="$BASE_DIR/.claude/skills"
    ;;
  opencode)
    TARGET_DIR="$HOME/.config/opencode/skills"
    ;;
  opencode-project)
    BASE_DIR="${CUSTOM_PATH:-.}"
    TARGET_DIR="$BASE_DIR/.opencode/skills"
    ;;
  custom)
    if [ -z "$CUSTOM_PATH" ]; then
      echo -e "${RED}Error: Custom directory path must be provided.${RESET}"
      exit 1
    fi
    TARGET_DIR="$CUSTOM_PATH"
    ;;
esac

echo -e "\n${BOLD}Target Directory:${RESET} ${CYAN}$TARGET_DIR${RESET}"
echo -e "${BOLD}Selected Capabilities:${RESET}  ${#SELECTED_SKILLS[@]} of ${#ALL_SKILLS[@]} (${SELECTED_SKILLS[*]})\n"

if [ "$DRY_RUN" = true ]; then
  echo -e "${YELLOW}[DRY RUN] No files will be modified.${RESET}"
fi

# Create target directory if needed
if [ "$DRY_RUN" = false ]; then
  mkdir -p "$TARGET_DIR"
fi

installed_count=0
for skill in "${SELECTED_SKILLS[@]}"; do
  skill=$(echo "$skill" | xargs)
  SRC_PATH=$(resolve_skill_dir "$skill")

  if [ -z "$SRC_PATH" ] || [ ! -d "$SRC_PATH" ]; then
    echo -e "  ${YELLOW}Warning: Capability '$skill' not found. Skipping.${RESET}"
    continue
  fi

  DEST_PATH="$TARGET_DIR/$skill"
  echo -e "  ${GREEN}Installing${RESET} ${BOLD}$skill${RESET}..."

  if [ "$DRY_RUN" = false ]; then
    mkdir -p "$DEST_PATH"
    if command -v rsync >/dev/null 2>&1; then
      rsync -a --delete \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='node_modules' \
        --exclude='.DS_Store' \
        --exclude='.court' \
        --exclude='.impeccable' \
        --exclude='.rigor' \
        --exclude='.artist' \
        "$SRC_PATH/" "$DEST_PATH/"
    else
      rm -rf "$DEST_PATH"
      cp -r "$SRC_PATH" "$DEST_PATH"
      find "$DEST_PATH" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
      find "$DEST_PATH" -type f -name "*.pyc" -delete 2>/dev/null || true
    fi

    # Set executable flags on scripts
    find "$DEST_PATH" -type f \( -name "*.py" -o -name "*.sh" -o -name "*.cjs" -o -name "*.js" \) -exec chmod +x {} + 2>/dev/null || true
  fi

  installed_count=$((installed_count + 1))
done

echo -e "\n${BOLD}${GREEN}Successfully installed $installed_count capability(ies) into $TARGET_DIR${RESET}\n"

if [ "$RUN_TESTS" = true ]; then
  if [ -f "$SCRIPT_DIR/test_all.py" ]; then
    echo -e "${BOLD}Running test suite verification...${RESET}"
    python3 -B "$SCRIPT_DIR/test_all.py" || true
  fi
fi
