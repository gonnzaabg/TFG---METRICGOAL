import duckdb
import pandas as pd

con = duckdb.connect("md:metricgoal_md?motherduck_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImdvbnphbG9ib3UuMjAyMy5hbHVtbkBjZXNjcmlzdG9yZXkuY29tIiwibWRSZWdpb24iOiJhd3MtZXUtY2VudHJhbC0xIiwic2Vzc2lvbiI6ImdvbnphbG9ib3UuMjAyMy5hbHVtbi5jZXNjcmlzdG9yZXkuY29tIiwicGF0IjoidUg3VGdkZGxpUWxkWmFUTE9KbjhZZnlFVy1ZX3N4UDZWOWY4TGJrZzdibyIsInVzZXJJZCI6ImFkNTUyNzA0LTZiMTItNGUxMC1iNWI0LWFhMjE2NTk2OWM5YiIsImlzcyI6Im1kX3BhdCIsInJlYWRPbmx5IjpmYWxzZSwidG9rZW5UeXBlIjoicmVhZF93cml0ZSIsImlhdCI6MTc3NzM5Nzk4NH0.uf4GkffqKpWZawH0QwlxgY2FGD1EeDze66QeUBULxyc")

df = pd.read_csv(r"C:\Users\Gonzalo\Desktop\TFG---METRICGOAL\METRICGOAL\Servidor\Scripts\BD_METRICGOAL - Hoja 1.csv")
con.execute("DROP TABLE IF EXISTS profesionales")
con.register("df_profesionales", df)
con.execute("CREATE TABLE profesionales AS SELECT * FROM df_profesionales")
print("✅ Profesionales:", con.execute("SELECT COUNT(*) FROM profesionales").fetchone())