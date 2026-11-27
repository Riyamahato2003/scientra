import { expect, test } from "@playwright/test";

test("foundation displays real API and database readiness", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Scientra", exact: true })).toBeVisible();
  await expect(page.getByRole("status")).toHaveText("API and database connected");
  await expect(page.getByText("Development foundation only.", { exact: false })).toBeVisible();
});
