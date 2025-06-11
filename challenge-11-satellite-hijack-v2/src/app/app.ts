#!/usr/bin/env bun
import { readFileSync, existsSync } from "fs";
import { join } from "path";
import { Elysia, t } from "elysia";
import { staticPlugin } from "@elysiajs/static";
import { file, type BunFile } from "bun";
import { html } from "@elysiajs/html";
import { jwt } from "@elysiajs/jwt";
import crypto from "crypto";
import * as cheerio from "cheerio";

const newUser = (max: number = 999_999_999) => {
  return Math.floor(Math.random() * max).toString();
};

const hashed = (data: string) => Bun.hash(data).toString();

const secretKeys = (() => {
  const keysPath = join(import.meta.dir, "secret_keys.txt");
  if (existsSync(keysPath)) {
    return (
      readFileSync(keysPath, "utf8")
      .trim()
      .split('\n')
      .map(key => key.trim())
      .filter(key => key.length >= 32)
    );
  }
  return [1, 2, 3].map(() => {
    crypto.randomBytes(32).toString('hex')
  });
})();

const flag = (() => {
  const flagPath = join(import.meta.dir, "flag.txt");
  if (existsSync(flagPath)) {
    return readFileSync(flagPath, "utf8").trim();
  }
  return "FLAG{example-flag-for-testing}";
})();

const app = new Elysia()
  .use(
    staticPlugin({
      assets: "public",
      prefix: "/",
    })
  )
  .use(html())
  .use(
    jwt({
      name: "jwt",
      secret: crypto.randomBytes(64).toString('hex')
    })
  )
  .decorate("layout", () => file("pages/layout.html"))
  .decorate("home", () => file("pages/home.html"))
  .decorate("satellites", () => file("pages/satellites.html"))
  .decorate("salad", () => file("pages/salad.html"))
  .decorate("tracking", () => file("pages/tracking.html"))
  .decorate("system", () => file("pages/system.html"))
  .decorate("about", () => file("pages/about.html"))
  .decorate("flagPage", () => file("pages/flag.html"))
  .guard(
    {
      headers: t.Object({
        user: t.Optional(t.String()),
      }),
      cookie: t.Cookie({
        token: t.Optional(t.String()),
      }),
    },
    (app) =>
      app
        .resolve(async ({ headers, cookie, jwt }) => {
          let userId = newUser();
          let authorized = false;

          if (headers.user) {
            const [user, key_id, tag] = headers.user.split(":");
            const key = secretKeys[key_id] ? secretKeys[key_id] : null;
            if (key && hashed(`${user}:${key}`).toString() === tag) {
              authorized = true;
            }

            userId = user;
          }

          if (cookie.token.value) {
            const verification = await jwt.verify(cookie.token.value);

            if (verification) {
              authorized = verification.authorized == "y";
              userId = verification.userId.toString();
            } else {
              cookie.token.remove();
            }
          } else {
            cookie.token.value = await jwt.sign({
              userId,
              authorized: authorized ? "y" : "n",
            });
          }
          
          let keyHash = hashed(secretKeys[userId % secretKeys.length]).toString();
          return { userId, keyHash, authorized };
        })
        .get(
          "/",
          async ({ layout, home, userId, keyHash }) => {
            const $ = cheerio.load(Buffer.from(await layout().arrayBuffer()));

            $("#user").html(userId);
            $("#coordinates").html(keyHash);
            $(".link").removeClass("has-text-link");
            $("#home-link").addClass("has-text-link");

            $("#content").html(await home().text());
            return $.html();
          },
          {
            headers: t.Object({
              user: t.Optional(t.String()),
            }),
            cookie: t.Cookie({
              user: t.Optional(t.String()),
            }),
          }
        )
        .get("/satellites", async ({ layout, satellites, userId, keyHash }) => {
          const $ = cheerio.load(Buffer.from(await layout().arrayBuffer()));

          $("#user").html(userId);
          $("#coordinates").html(keyHash);
          $(".link").removeClass("has-text-link");
          $("#satellites-link").addClass("has-text-link");

          $("#content").html(await satellites().text());
          return $.html();
        })
        .get("/salad", async ({ layout, salad, userId, keyHash }) => {
          const $ = cheerio.load(Buffer.from(await layout().arrayBuffer()));

          $("#user").html(userId);
          $("#coordinates").html(keyHash);
          $(".link").removeClass("has-text-link");

          $("#content").html(await salad().text());
          return $.html();
        })
        .get("/tracking", async ({ layout, tracking, userId, keyHash }) => {
          const $ = cheerio.load(Buffer.from(await layout().arrayBuffer()));

          $("#user").html(userId);
          $("#coordinates").html(keyHash);
          $(".link").removeClass("has-text-link");
          $("#tracking-link").addClass("has-text-link");

          $("#content").html(await tracking().text());
          return $.html();
        })
        .get("/system", async ({ layout, system, userId, keyHash }) => {
          const $ = cheerio.load(Buffer.from(await layout().arrayBuffer()));

          $("#user").html(userId);
          $("#coordinates").html(keyHash);
          $(".link").removeClass("has-text-link");
          $("#system-link").addClass("has-text-link");

          $("#content").html(await system().text());
          return $.html();
        })
        .get("/about", async ({ layout, about, userId, keyHash, authorized }) => {
          const $ = cheerio.load(Buffer.from(await layout().arrayBuffer()));

          $("#user").html(userId);
          $("#coordinates").html(keyHash);
          $(".link").removeClass("has-text-link");
          $("#about-link").addClass("has-text-link");

          $("#content").html(await about().text());

          if (authorized) {
            $("#explore").append(
              `<a class="button is-info is-light" href="/flag" id="flag-link">Beam Flag from Satellite </a>`
            );
          }
          return $.html();
        })
        .get(
          "/flag",
          async ({ layout, flagPage, userId, keyHash, authorized, redirect }) => {
            if (!authorized) return redirect("/");

            const $ = cheerio.load(Buffer.from(await layout().arrayBuffer()));

            $("#user").html(userId);
            $("#coordinates").html(keyHash);
            $(".link").removeClass("has-text-link");
            $("#flag-link").addClass("has-text-link");

            $("#content").html(await flagPage().text());
            $("#flag").html(flag);
            return $.html();
          }
        )
        .post(
          "/hash",
          ({ body }) => {
            return {
              hash: body.data.includes(", ")
                ? body.data.split(", ").map((x) => hashed(x))
                : hashed(body.data),
            };
          },
          {
            body: t.Object({
              data: t.String(),
            }),
          }
        )
  )
  .onError(({ code, error }) => {
    return redirect("/")
  });

// Start App
const port = process.env.APP_PORT || 8000;
app.listen(port);

console.log(`Launching Satellite on port: ${port}`);
