#!/usr/bin/env bun
import { readFileSync, existsSync } from "fs";
import { join } from "path";
import { Elysia, t } from "elysia";
import { staticPlugin } from "@elysiajs/static";
import { file, type BunFile } from "bun";
import { html } from "@elysiajs/html";
import * as cheerio from "cheerio";

const newUser = (max: number = 999_999_999) => {
  return Math.floor(Math.random() * max).toString();
};

const hashed = (data: string) => Bun.hash(data).toString();

const secret = "2842816338533097556";

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
  .decorate("layout", () => file("pages/layout.html"))
  .decorate("home", () => file("pages/home.html"))
  .decorate("satellites", () => file("pages/satellites.html"))
  .decorate("about", () => file("pages/about.html"))
  .decorate("flagPage", () => file("pages/flag.html"))
  .guard(
    {
      headers: t.Object({
        user: t.Optional(t.String()),
      }),
      cookie: t.Cookie({
        user: t.Optional(t.String()),
      }),
    },
    (app) =>
      app
        .resolve(({ headers, cookie }) => {
          let userId = newUser(),
            authorized = false;

          if (headers.user) {
            userId = headers.user;
          }

          if (cookie.user.value) {
            try {
              userId = atob(cookie.user.value);
            } catch (e) {
              userId = newUser();
            }
          }

          authorized = hashed(userId) === secret;

          cookie.user.value = btoa(userId);
          return { userId, authorized };
        })
        .get(
          "/",
          async ({ layout, home, userId }) => {
            const $ = cheerio.load(Buffer.from(await layout().arrayBuffer()));

            $("#user").html(userId);
            $(".link").removeClass("has-text-info");
            $("#home-link").addClass("has-text-info");

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
        .get("/satellites", async ({ layout, satellites, userId }) => {
          const $ = cheerio.load(Buffer.from(await layout().arrayBuffer()));

          $("#user").html(userId);
          $(".link").removeClass("has-text-info");
          $("#satellites-link").addClass("has-text-info");

          $("#content").html(await satellites().text());
          return $.html();
        })
        .get("/about", async ({ layout, about, userId, authorized }) => {
          const $ = cheerio.load(Buffer.from(await layout().arrayBuffer()));

          $("#user").html(userId);
          $(".link").removeClass("has-text-info");
          $("#about-link").addClass("has-text-info");

          $("#content").html(await about().text());
          if (authorized) {
            $("#explore").append(
              `<a class="button is-info is-light" href="/flag" id="flag-link">Download Flag from Satellite</a>`
            );
          }
          return $.html();
        })
        .get(
          "/flag",
          async ({ layout, flagPage, userId, authorized, redirect }) => {
            if (!authorized) return redirect("/");

            const $ = cheerio.load(Buffer.from(await layout().arrayBuffer()));

            $("#user").html(userId);
            $(".link").removeClass("has-text-info");
            $("#flag-link").addClass("has-text-info");

            $("#content").html(await flagPage().text());
            $("#flag").html(flag);
            return $.html();
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
