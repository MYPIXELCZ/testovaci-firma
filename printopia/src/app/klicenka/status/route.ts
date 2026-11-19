import { klicenkaStatus } from "@mypixel/klicenka/next";

export const GET = klicenkaStatus("cookie", {
  audience: process.env.KLICENKA_AUDIENCE ?? "printopia",
  environment: process.env.KLICENKA_ENVIRONMENT ?? "production",
});
