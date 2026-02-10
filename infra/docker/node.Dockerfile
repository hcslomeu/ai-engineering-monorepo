# ---- Stage 1: Dependencies ----
FROM node:22-slim AS deps

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# Copy dependency manifests first (cache-friendly layer ordering)
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
# Future: uncomment as workspace packages are created
# COPY apps/alpha-whale/web/package.json apps/alpha-whale/web/
# COPY libs/shared-schemas/package.json libs/shared-schemas/

RUN --mount=type=cache,target=/pnpm/store \
    pnpm install --frozen-lockfile


# ---- Stage 2: Builder ----
FROM deps AS builder

WORKDIR /app

# Copy all source code (deps already installed from previous stage)
COPY . .

# Future: build the Next.js app (requires WP-004)
# RUN pnpm nx build alpha-whale-web


# ---- Stage 3: Runtime ----
FROM node:22-slim AS runtime

ENV NODE_ENV=production

WORKDIR /app

# Future: copy Next.js standalone output (requires WP-004)
# COPY --from=builder /app/apps/alpha-whale/web/.next/standalone ./
# COPY --from=builder /app/apps/alpha-whale/web/.next/static ./.next/static
# COPY --from=builder /app/apps/alpha-whale/web/public ./public

# Non-root user for security (node:22-slim ships with a 'node' user at UID/GID 1000)
RUN chown -R node:node /app

USER node

EXPOSE 3000

# Future: start the Next.js standalone server
# CMD ["node", "server.js"]
CMD ["node", "--version"]
